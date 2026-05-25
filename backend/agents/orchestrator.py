import json
import time
import logging
from pathlib import Path
from groq import Groq
from backend.schemas import (
    OrchestratorOutput, TrajectoryOutput, ContextOutput,
    InterventionOutput, EffectivenessOutput, Decision, Severity,
)

logger = logging.getLogger("sentinel.agents.orchestrator")
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "orchestrator.md"


async def run_orchestrator_agent(
    trajectory: TrajectoryOutput, context: ContextOutput,
    intervention: InterventionOutput, effectiveness: EffectivenessOutput,
    profile: dict, groq_client: Groq,
) -> tuple[OrchestratorOutput, float]:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    user_msg = f"""Synthesize all agent outputs into a final recommendation.

Player: {profile.get('riot_id', 'Unknown')}
Game: {profile.get('game', 'lol')}
Account age: {profile.get('account_age_days', 0)} days

Trajectory Agent:
{json.dumps(trajectory.model_dump(), indent=2)}

Context Agent:
{json.dumps(context.model_dump(), indent=2)}

Intervention Agent:
{json.dumps(intervention.model_dump(), indent=2)}

Effectiveness Agent:
{json.dumps(effectiveness.model_dump(), indent=2)}"""

    start = time.time()
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
            temperature=0.3, max_tokens=800, response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        latency_ms = (time.time() - start) * 1000
        data = json.loads(raw)
        data["decision"] = data.get("decision", "MONITOR").upper().replace(" ", "_")
        data["severity"] = data.get("severity", "MEDIUM").upper()
        return OrchestratorOutput(**data), latency_ms
    except Exception as e:
        logger.error(f"Orchestrator error: {e}, retrying")
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt + "\n\nCRITICAL: Output ONLY valid JSON."},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.2, max_tokens=800, response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content
            latency_ms = (time.time() - start) * 1000
            data = json.loads(raw)
            data["decision"] = data.get("decision", "MONITOR").upper().replace(" ", "_")
            data["severity"] = data.get("severity", "MEDIUM").upper()
            return OrchestratorOutput(**data), latency_ms
        except Exception as e2:
            latency_ms = (time.time() - start) * 1000
            return OrchestratorOutput(
                decision=Decision.MONITOR, severity=Severity.MEDIUM, confidence=0.0,
                executive_summary="Orchestrator error. Manual review required.",
                recommended_actions=["Manual review of all agent outputs"],
                dissent_notes="Orchestrator failed.", explainability_trail=["Automated orchestration failed"],
            ), latency_ms
