from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Game(str, Enum):
    LOL = "lol"
    VALORANT = "valorant"


class DataMode(str, Enum):
    LIVE = "live"
    CACHED = "cached"
    DEMO = "demo"


class Decision(str, Enum):
    NO_ACTION = "NO_ACTION"
    NUDGE = "NUDGE"
    ADJUST = "ADJUST"
    MONITOR = "MONITOR"
    ESCALATE = "ESCALATE"


class Severity(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TrajectoryDirection(str, Enum):
    STABLE = "stable"
    DECLINING = "declining"
    RECOVERING = "recovering"
    SPIRALING = "spiraling"


class ReviewRequest(BaseModel):
    game: Game
    riot_id: str
    region: str = "americas"
    platform: str = "na1"


class TrajectoryOutput(BaseModel):
    current_health: float = Field(ge=0.0, le=1.0)
    baseline_health: float = Field(ge=0.0, le=1.0)
    predicted_health_3_sessions: float = Field(ge=0.0, le=1.0)
    trajectory_direction: str = "stable"
    decline_velocity: float = Field(ge=0.0, le=1.0, default=0.0)
    tilt_indicators: list[str] = []
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = ""


class ContextOutput(BaseModel):
    primary_trigger: str = ""
    contributing_factors: list[str] = []
    temporal_pattern: str = ""
    emotional_state_estimate: str = ""
    trigger_confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = ""


class InterventionOutput(BaseModel):
    recommended_intervention: str = ""
    intervention_type: str = ""
    urgency: str = "LOW"
    specific_actions: list[str] = []
    expected_effectiveness: float = Field(ge=0.0, le=1.0)
    reasoning: str = ""


class EffectivenessOutput(BaseModel):
    false_positive_risk: float = Field(ge=0.0, le=1.0)
    intervention_appropriateness: float = Field(ge=0.0, le=1.0)
    harm_if_wrong: str = ""
    historical_success_rate: float = Field(ge=0.0, le=1.0)
    alternative_explanations: list[str] = []
    reasoning: str = ""


class OrchestratorOutput(BaseModel):
    decision: Decision
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    executive_summary: str = ""
    recommended_actions: list[str] = []
    dissent_notes: str = ""
    explainability_trail: list[str] = []


class ReviewResponse(BaseModel):
    id: str
    timestamp: str
    game: Game
    riot_id: str
    region: str
    data_mode: DataMode
    trajectory: TrajectoryOutput
    context: ContextOutput
    intervention: InterventionOutput
    effectiveness: EffectivenessOutput
    orchestrator: OrchestratorOutput


class DataModeStatus(BaseModel):
    mode: DataMode
    riot_api_healthy: bool
    last_check: Optional[str] = None
    message: str = ""
