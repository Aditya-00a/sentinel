import json
import time
import logging
from pathlib import Path
from groq import Groq
from backend.schemas import InterventionOutput

logger = logging.getLogger("sentinel.agents.intervention")
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "network.md"


def _extract_intervention_signals(profile: dict, trajectory_result: dict, context_result: dict) -> dict:
    return {
        "player_name": profile.get("riot_id", "Unknown"),
        "game": profile.get("game", "lol"),
        "account_age_days": profile.get("account_age_days", 0),
        "honor_level": profile.get("honor_level", 2),
        "trajectory_analysis": trajectory_result,
        "context_analysis": context_result,
        "intervention_history": profile.get("intervention_history", []),
        "report_count": profile.get("report_count", 0),
    }


async def run_intervention_agent(
    profile: dict, game: str, trajectory_result: dict, context_result: dict, groq_client: Groq
) -> tuple[InterventionOutput, float]:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    signals = _extract_intervention_signals(profile, trajectory_result, context_result)
    user_msg = f"Recommend an intervention for this player based on their trajectory and context.\n\nPlayer data:\n{json.dumps(signals, indent=2)}"

    start = time.time()
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
            temperature=0.2, max_tokens=800, response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        latency_ms = (time.time() - start) * 1000
        return InterventionOutput(**json.loads(raw)), latency_ms
    except Exception as e:
        logger.error(f"Intervention agent error: {e}, retrying")
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
            return InterventionOutput(**json.loads(raw)), latency_ms
        except Exception as e2:
            latency_ms = (time.time() - start) * 1000
            return InterventionOutput(
                recommended_intervention="Manual review", intervention_type="MONITORED_PLAY",
                urgency="LOW", specific_actions=["Agent error — manual review recommended"],
                expected_effectiveness=0.0, reasoning=f"Agent error: {str(e2)[:100]}"
            ), latency_ms
