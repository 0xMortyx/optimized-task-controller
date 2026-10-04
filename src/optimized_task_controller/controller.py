import json
from pathlib import Path
from .models import Decision, RoutingReceipt, Task
from .scoring import value_score

class OptimizedTaskController:
    def __init__(self, config_path: str | None = None):
        if config_path is None:
            config_path = Path(__file__).resolve().parents[2] / "config" / "controller.json"
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def decide(self, task: Task) -> RoutingReceipt:
        t = self.config["thresholds"]
        w = self.config["weights"]
        score = value_score(task, w)

        if task.irreversible or task.risk >= t["human_risk"]:
            return RoutingReceipt(Decision.HUMAN, score, "high-risk or irreversible action requires approval")

        if task.redundancy >= t["cache_redundancy"]:
            return RoutingReceipt(Decision.CACHE, score, "task is sufficiently redundant to reuse a known answer")

        if score <= t["drop_value"] and task.urgency < 0.5:
            return RoutingReceipt(Decision.DROP, score, "task value is below the execution threshold")

        if task.urgency <= t["batch_urgency"] and task.complexity < t["frontier_complexity"]:
            return RoutingReceipt(Decision.BATCH, score, "valuable but non-urgent task can wait for batch execution")

        if task.complexity >= t["frontier_complexity"] or score >= t["frontier_value"]:
            return RoutingReceipt(Decision.FRONTIER_MODEL, score, "task requires higher reasoning capacity", "frontier")

        return RoutingReceipt(Decision.SMALL_MODEL, score, "small model is the cheapest capable tier", "small")
