import json
import time
import logging
from pathlib import Path
from groq import Groq
from schemas import EffectivenessOutput, TrajectoryOutput, ContextOutput, InterventionOutput

logger = logging.getLogger("sentinel.agents.effectiveness")
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "compliance.md"


async def run_effectiveness_agent(
    trajectory: TrajectoryOutput, context: ContextOutput, intervention: InterventionOutput,
    profile: dict, groq_client: Groq,
) -> tuple[EffectivenessOutput, float]:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    user_msg = f"""Evaluate this intervention recommendation for appropriateness and false-positive risk.

Trajectory Agent Output:
{json.dumps(trajectory.model_dump(), indent=2)}

Context Agent Output:
{json.dumps(context.model_dump(), indent=2)}

Intervention Agent Output:
{json.dumps(intervention.model_dump(), indent=2)}

Player context:
- Account age: {profile.get('account_age_days', 0)} days
- Honor level: {profile.get('honor_level', 2)}
- Report count: {profile.get('report_count', 0)}
- Intervention history: {json.dumps(profile.get('intervention_history', []), indent=2)}"""

    start = time.time()
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
            temperature=0.15, max_tokens=800, response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        latency_ms = (time.time() - start) * 1000
        return EffectivenessOutput(**json.loads(raw)), latency_ms
    except Exception as e:
        logger.error(f"Effectiveness agent error: {e}, retrying")
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
            return EffectivenessOutput(**json.loads(raw)), latency_ms
        except Exception as e2:
            latency_ms = (time.time() - start) * 1000
            return EffectivenessOutput(
                false_positive_risk=0.5, intervention_appropriateness=0.5,
                harm_if_wrong="MEDIUM", historical_success_rate=0.5,
                alternative_explanations=["Agent error — manual review required"],
                reasoning=f"Agent error: {str(e2)[:100]}"
            ), latency_ms
