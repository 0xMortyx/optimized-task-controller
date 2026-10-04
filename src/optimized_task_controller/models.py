from dataclasses import dataclass
from enum import Enum

class Decision(str, Enum):
    CACHE = "CACHE"
    SMALL_MODEL = "SMALL_MODEL"
    FRONTIER_MODEL = "FRONTIER_MODEL"
    BATCH = "BATCH"
    DROP = "DROP"
    HUMAN = "HUMAN"

@dataclass
class Task:
    text: str
    worth: float = 0.5
    novelty: float = 0.5
    urgency: float = 0.5
    complexity: float = 0.5
    redundancy: float = 0.0
    risk: float = 0.0
    irreversible: bool = False

@dataclass
class RoutingReceipt:
    decision: Decision
    score: float
    reason: str
    model_tier: str | None = None
