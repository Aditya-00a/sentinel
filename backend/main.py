import asyncio
import json
import logging
import os
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Make imports work in BOTH environments:
#   - Local dev: `python -m uvicorn backend.main:app` from project root
#     (backend/ is loaded as a package; we add backend/ itself to sys.path
#      so bare `from agents import ...` also resolves)
#   - Vercel:  experimentalServices mounts backend/ as the deployment root,
#     so there's no `backend` package at runtime — only bare modules work.
_here = Path(__file__).parent          # .../backend/  OR  /var/task on Vercel
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from groq import Groq
from sse_starlette.sse import EventSourceResponse

from agents import (
    run_trajectory_agent,
    run_context_agent,
    run_intervention_agent,
    run_effectiveness_agent,
    run_orchestrator_agent,
)
from db import init_db, save_review, save_audit, get_history, get_review
from demo_profiles import get_demo_profiles_summary, get_demo_profile, DEMO_PROFILES
from riot_api import (
    get_account_by_riot_id,
    get_summoner_by_puuid,
    get_match_ids_lol,
    get_match_detail_lol,
    get_match_ids_val,
    get_match_detail_val,
    check_api_health,
)
from schemas import ReviewRequest, DataMode

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel")

app = FastAPI(title="Sentinel", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def strip_vercel_prefix(request: Request, call_next):
    """Strip /_/backend prefix added by Vercel's experimentalServices routing."""
    path = request.scope.get("path", "")
    if path.startswith("/_/backend"):
        request.scope["path"] = path[len("/_/backend"):] or "/"
        request.scope["raw_path"] = request.scope["path"].encode()
    return await call_next(request)

rate_limit_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = 20
RATE_WINDOW = 60


@app.on_event("startup")
async def startup():
    init_db()
    logger.info("Sentinel v2 started — pre-escalation intelligence active")


def get_groq_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")
    return Groq(api_key=api_key)


def check_rate_limit(ip: str) -> bool:
    now = time.time()
    rate_limit_store[ip] = [t for t in rate_limit_store[ip] if now - t < RATE_WINDOW]
    if len(rate_limit_store[ip]) >= RATE_LIMIT:
        return False
    rate_limit_store[ip].append(now)
    return True


async def build_profile_from_riot(req: ReviewRequest) -> tuple[dict | None, DataMode]:
    parts = req.riot_id.split("#")
    if len(parts) != 2:
        return None, DataMode.DEMO

    game_name, tag_line = parts[0], parts[1]
    account = await get_account_by_riot_id(game_name, tag_line, req.region)
    if not account:
        return None, DataMode.DEMO

    puuid = account["puuid"]
    data_mode = DataMode.LIVE

    if req.game == "lol":
        summoner = await get_summoner_by_puuid(puuid, req.platform)
        match_ids = await get_match_ids_lol(puuid, req.platform, 10)
        if match_ids is None:
            data_mode = DataMode.CACHED
            match_ids = []

        matches = []
        for mid in (match_ids or []):
            detail = await get_match_detail_lol(mid, req.platform)
            if detail:
                matches.append(detail)

        # Build synthetic session data from real matches for trajectory analysis
        sessions = []
        for i, m in enumerate(matches):
            participants = m.get("info", {}).get("participants", [])
            player = next((p for p in participants if p.get("puuid") == puuid), None)
            if player:
                sessions.append({
                    "date": f"session-{i}",
                    "time_of_day": "unknown",
                    "matches_played": 1,
                    "behavioral_health": min(1.0, max(0.1, 0.5 + (player.get("kills", 0) - player.get("deaths", 0)) * 0.05)),
                    "reports_received": 0,
                    "honor_received": 0,
                    "surrender_votes_yes": 0,
                    "surrender_votes_total": 0,
                    "chat_flags": [],
                    "avg_kda": round((player.get("kills", 0) + player.get("assists", 0)) / max(player.get("deaths", 1), 1), 1),
                    "cs_per_min": round(player.get("totalMinionsKilled", 0) / max(m.get("info", {}).get("gameDuration", 1800) / 60, 1), 1),
                    "champions_played": [player.get("championName", "Unknown")],
                    "agents_played": [],
                })

        profile = {
            "riot_id": req.riot_id, "game": req.game, "region": req.region, "platform": req.platform,
            "account": {"puuid": puuid, "gameName": game_name, "tagLine": tag_line,
                        "summonerLevel": summoner.get("summonerLevel", 0) if summoner else 0},
            "rank": {}, "account_age_days": 0, "sessions": sessions,
            "trajectory": {"direction": "stable", "velocity": 0.0, "current_health": 0.5,
                           "predicted_health_3_sessions": 0.5, "baseline_health": 0.5, "tilt_trigger": "Unknown"},
            "intervention_history": [], "report_count": 0, "honor_level": 2,
        }
        return profile, data_mode
    else:
        match_ids = await get_match_ids_val(puuid, req.region)
        if match_ids is None:
            data_mode = DataMode.CACHED
            match_ids = []

        matches = []
        for mid in (match_ids or []):
            detail = await get_match_detail_val(mid, req.region)
            if detail:
                matches.append(detail)

        sessions = []
        for i, m in enumerate(matches):
            players = m.get("players", [])
            player = next((p for p in players if p.get("puuid") == puuid), None)
            if player:
                stats = player.get("stats", {})
                sessions.append({
                    "date": f"session-{i}", "time_of_day": "unknown", "matches_played": 1,
                    "behavioral_health": min(1.0, max(0.1, 0.5 + (stats.get("kills", 0) - stats.get("deaths", 0)) * 0.03)),
                    "reports_received": 0, "honor_received": 0, "surrender_votes_yes": 0, "surrender_votes_total": 0,
                    "chat_flags": [], "avg_kda": round((stats.get("kills", 0) + stats.get("assists", 0)) / max(stats.get("deaths", 1), 1), 1),
                    "headshot_pct": player.get("headshotPct", 0),
                    "champions_played": [], "agents_played": [player.get("characterId", "Unknown")],
                })

        profile = {
            "riot_id": req.riot_id, "game": req.game, "region": req.region, "platform": req.platform,
            "account": {"puuid": puuid, "gameName": game_name, "tagLine": tag_line},
            "rank": {}, "account_age_days": 0, "sessions": sessions,
            "trajectory": {"direction": "stable", "velocity": 0.0, "current_health": 0.5,
                           "predicted_health_3_sessions": 0.5, "baseline_health": 0.5, "tilt_trigger": "Unknown"},
            "intervention_history": [], "report_count": 0, "honor_level": 2,
        }
        return profile, data_mode


async def stream_review(profile: dict, game: str, data_mode: DataMode, review_id: str):
    groq_client = get_groq_client()
    timestamp = datetime.now(timezone.utc).isoformat()

    yield {"event": "status", "data": json.dumps({"stage": "started", "review_id": review_id, "data_mode": data_mode.value})}

    # Phase 1: Trajectory + Context in parallel
    trajectory_task = asyncio.create_task(run_trajectory_agent(profile, game, groq_client))
    context_task = asyncio.create_task(run_context_agent(profile, game, groq_client))

    yield {"event": "status", "data": json.dumps({"stage": "agents_running", "agents": ["trajectory", "context"]})}

    trajectory, trajectory_ms = await trajectory_task
    yield {"event": "agent_result", "data": json.dumps({"agent": "trajectory", "result": trajectory.model_dump(), "latency_ms": round(trajectory_ms)})}

    context, context_ms = await context_task
    yield {"event": "agent_result", "data": json.dumps({"agent": "context", "result": context.model_dump(), "latency_ms": round(context_ms)})}

    # Phase 2: Intervention uses trajectory + context results
    yield {"event": "status", "data": json.dumps({"stage": "intervention_running"})}
    intervention, intervention_ms = await run_intervention_agent(
        profile, game, trajectory.model_dump(), context.model_dump(), groq_client
    )
    yield {"event": "agent_result", "data": json.dumps({"agent": "intervention", "result": intervention.model_dump(), "latency_ms": round(intervention_ms)})}

    # Phase 3: Effectiveness audits everything
    yield {"event": "status", "data": json.dumps({"stage": "effectiveness_running"})}
    effectiveness, effectiveness_ms = await run_effectiveness_agent(
        trajectory, context, intervention, profile, groq_client
    )
    yield {"event": "agent_result", "data": json.dumps({"agent": "effectiveness", "result": effectiveness.model_dump(), "latency_ms": round(effectiveness_ms)})}

    # Phase 4: Orchestrator synthesizes
    yield {"event": "status", "data": json.dumps({"stage": "orchestrator_running"})}
    orchestrator, orchestrator_ms = await run_orchestrator_agent(
        trajectory, context, intervention, effectiveness, profile, groq_client
    )
    yield {"event": "agent_result", "data": json.dumps({"agent": "orchestrator", "result": orchestrator.model_dump(), "latency_ms": round(orchestrator_ms)})}

    review = {
        "id": review_id, "timestamp": timestamp, "game": game,
        "riot_id": profile.get("riot_id", "Unknown"), "region": profile.get("region", "americas"),
        "data_mode": data_mode.value,
        "trajectory": trajectory.model_dump(), "context": context.model_dump(),
        "intervention": intervention.model_dump(), "effectiveness": effectiveness.model_dump(),
        "orchestrator": orchestrator.model_dump(),
    }

    save_review(review)
    for name, output, latency in [
        ("trajectory", trajectory.model_dump(), trajectory_ms),
        ("context", context.model_dump(), context_ms),
        ("intervention", intervention.model_dump(), intervention_ms),
        ("effectiveness", effectiveness.model_dump(), effectiveness_ms),
        ("orchestrator", orchestrator.model_dump(), orchestrator_ms),
    ]:
        save_audit(review_id, name, {}, output, latency, timestamp)

    yield {"event": "complete", "data": json.dumps(review)}


@app.post("/api/review")
async def review_player(req: ReviewRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    review_id = str(uuid.uuid4())
    profile, data_mode = await build_profile_from_riot(req)

    if profile is None or not profile.get("sessions"):
        for demo in DEMO_PROFILES.values():
            if demo["game"] == req.game:
                profile = demo
                data_mode = DataMode.DEMO
                break
        if profile is None:
            profile = list(DEMO_PROFILES.values())[0]
            data_mode = DataMode.DEMO

    return EventSourceResponse(stream_review(profile, req.game, data_mode, review_id))


@app.post("/api/review-demo/{profile_id}")
async def review_demo(profile_id: str, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    profile = get_demo_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Demo profile not found")

    review_id = str(uuid.uuid4())
    return EventSourceResponse(stream_review(profile, profile["game"], DataMode.DEMO, review_id))


@app.get("/api/demo-profiles")
async def demo_profiles():
    return get_demo_profiles_summary()


@app.get("/api/history")
async def history():
    return get_history(20)


@app.get("/api/review/{review_id}")
async def get_review_detail(review_id: str):
    review = get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@app.get("/api/data-mode")
async def data_mode():
    healthy = await check_api_health()
    riot_key = bool(os.environ.get("RIOT_API_KEY", ""))
    if healthy:
        mode = DataMode.LIVE
        msg = "Riot API responding. Live trajectory data available."
    elif riot_key:
        mode = DataMode.CACHED
        msg = "Riot API key set but not responding. Cached/demo data."
    else:
        mode = DataMode.DEMO
        msg = "Demo mode. Pre-built behavioral trajectories."
    return {"mode": mode.value, "riot_api_healthy": healthy, "riot_key_set": riot_key, "message": msg}


@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0", "timestamp": datetime.now(timezone.utc).isoformat()}


STATIC_DIR = Path(__file__).parent.parent / "frontend" / "dist"
if STATIC_DIR.exists():
    from starlette.responses import FileResponse

    assets_dir = STATIC_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        if path.startswith("api/"):
            raise HTTPException(status_code=404)
        file_path = STATIC_DIR / path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
