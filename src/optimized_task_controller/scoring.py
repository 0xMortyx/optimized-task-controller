from .models import Task

def value_score(task: Task, weights: dict) -> float:
    score = (
        task.worth * weights["worth"]
        + task.novelty * weights["novelty"]
        + task.urgency * weights["urgency"]
        + task.complexity * weights["complexity"]
        - task.redundancy * weights["redundancy_penalty"]
    )
    return max(0.0, min(1.0, score))
