import json
import time
import logging
from pathlib import Path
from groq import Groq
from backend.schemas import TrajectoryOutput

logger = logging.getLogger("sentinel.agents.trajectory")
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "behavior.md"


def _extract_trajectory_signals(profile: dict) -> dict:
    sessions = profile.get("sessions", [])
    trajectory = profile.get("trajectory", {})

    health_scores = [s["behavioral_health"] for s in sessions if "behavioral_health" in s]
    chat_flags_total = sum(len(s.get("chat_flags", [])) for s in sessions)
    reports_total = sum(s.get("reports_received", 0) for s in sessions)
    honor_total = sum(s.get("honor_received", 0) for s in sessions)
    surrender_yes = sum(s.get("surrender_votes_yes", 0) for s in sessions)

    time_of_day_distribution = {}
    for s in sessions:
        tod = s.get("time_of_day", "unknown")
        time_of_day_distribution[tod] = time_of_day_distribution.get(tod, 0) + 1

    champions_across = {}
    for s in sessions:
        for c in s.get("champions_played", []) + s.get("agents_played", []):
            champions_across[c] = champions_across.get(c, 0) + 1

    return {
        "player_name": profile.get("riot_id", "Unknown"),
        "game": profile.get("game", "lol"),
        "account_age_days": profile.get("account_age_days", 0),
        "rank": profile.get("rank", {}),
        "total_sessions": len(sessions),
        "health_score_timeline": health_scores,
        "trajectory_metadata": trajectory,
        "total_chat_flags": chat_flags_total,
        "total_reports_received": reports_total,
        "total_honor_received": honor_total,
        "total_surrender_votes_yes": surrender_yes,
        "time_of_day_distribution": time_of_day_distribution,
        "champion_agent_diversity": len(champions_across),
        "most_played": sorted(champions_across.items(), key=lambda x: -x[1])[:3],
        "session_details": [
            {
                "date": s.get("date"),
                "time": s.get("time_of_day"),
                "matches": s.get("matches_played", 0),
                "health": s.get("behavioral_health", 0),
                "reports": s.get("reports_received", 0),
                "honor": s.get("honor_received", 0),
                "chat_flags": s.get("chat_flags", []),
                "avg_kda": s.get("avg_kda", 0),
            }
            for s in sessions
        ],
        "honor_level": profile.get("honor_level", 2),
        "report_count": profile.get("report_count", 0),
    }


async def run_trajectory_agent(profile: dict, game: str, groq_client: Groq) -> tuple[TrajectoryOutput, float]:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    signals = _extract_trajectory_signals(profile)
    user_msg = f"Analyze this player's behavioral health trajectory.\n\nPlayer data:\n{json.dumps(signals, indent=2)}"

    start = time.time()
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
            temperature=0.2, max_tokens=800, response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        latency_ms = (time.time() - start) * 1000
        return TrajectoryOutput(**json.loads(raw)), latency_ms
    except Exception as e:
        logger.error(f"Trajectory agent error: {e}, retrying")
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt + "\n\nCRITICAL: Output ONLY valid JSON. No other text."},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.1, max_tokens=800, response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content
            latency_ms = (time.time() - start) * 1000
            return TrajectoryOutput(**json.loads(raw)), latency_ms
        except Exception as e2:
            latency_ms = (time.time() - start) * 1000
            return TrajectoryOutput(
                current_health=0.5, baseline_health=0.5, predicted_health_3_sessions=0.5,
                trajectory_direction="stable", decline_velocity=0.0,
                tilt_indicators=["Agent error — manual review recommended"],
                confidence=0.0, reasoning=f"Agent error: {str(e2)[:100]}"
            ), latency_ms
