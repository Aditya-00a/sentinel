import json
import time
import logging
from pathlib import Path
from groq import Groq
from schemas import ContextOutput

logger = logging.getLogger("sentinel.agents.context")
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "performance.md"


def _extract_context_signals(profile: dict) -> dict:
    sessions = profile.get("sessions", [])
    trajectory = profile.get("trajectory", {})

    time_health_pairs = []
    for s in sessions:
        time_health_pairs.append({
            "date": s.get("date"), "time": s.get("time_of_day"),
            "health": s.get("behavioral_health", 0), "matches": s.get("matches_played", 0),
            "kda": s.get("avg_kda", 0), "chat_flags": s.get("chat_flags", []),
            "champions": s.get("champions_played", []) + s.get("agents_played", []),
        })

    signals = {
        "player_name": profile.get("riot_id", "Unknown"),
        "game": profile.get("game", "lol"),
        "account_age_days": profile.get("account_age_days", 0),
        "rank": profile.get("rank", {}),
        "stated_tilt_trigger": trajectory.get("tilt_trigger", ""),
        "session_timeline": time_health_pairs,
        "intervention_history": profile.get("intervention_history", []),
    }

    if profile.get("duo_sessions"):
        signals["duo_sessions"] = profile["duo_sessions"]
        signals["solo_sessions"] = profile.get("solo_sessions", [])

    if profile.get("role_swap_detected"):
        signals["role_swap_detected"] = profile["role_swap_detected"]

    return signals


async def run_context_agent(profile: dict, game: str, groq_client: Groq) -> tuple[ContextOutput, float]:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    signals = _extract_context_signals(profile)
    user_msg = f"Identify what's driving this player's behavioral trajectory.\n\nPlayer data:\n{json.dumps(signals, indent=2)}"

    start = time.time()
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
            temperature=0.2, max_tokens=800, response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        latency_ms = (time.time() - start) * 1000
        return ContextOutput(**json.loads(raw)), latency_ms
    except Exception as e:
        logger.error(f"Context agent error: {e}, retrying")
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt + "\n\nCRITICAL: Output ONLY valid JSON."},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.1, max_tokens=800, response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content
            latency_ms = (time.time() - start) * 1000
            return ContextOutput(**json.loads(raw)), latency_ms
        except Exception as e2:
            latency_ms = (time.time() - start) * 1000
            return ContextOutput(
                primary_trigger="Unable to determine", contributing_factors=["Agent error"],
                temporal_pattern="Unknown", emotional_state_estimate="Unknown",
                trigger_confidence=0.0, reasoning=f"Agent error: {str(e2)[:100]}"
            ), latency_ms
