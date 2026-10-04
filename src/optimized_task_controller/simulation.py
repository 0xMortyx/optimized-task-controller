from collections import Counter
import random
from .models import Task
from .controller import OptimizedTaskController

DEMO_DISTRIBUTION = {
    "SMALL_MODEL": 0.548,
    "BATCH": 0.182,
    "CACHE": 0.114,
    "FRONTIER_MODEL": 0.086,
    "DROP": 0.054,
    "HUMAN": 0.016,
}

def demo_distribution(n: int = 8400) -> Counter:
    labels = list(DEMO_DISTRIBUTION)
    weights = list(DEMO_DISTRIBUTION.values())
    rng = random.Random(42)
    return Counter(rng.choices(labels, weights=weights, k=n))

def organic_simulation(n: int = 1000, seed: int = 42) -> Counter:
    rng = random.Random(seed)
    controller = OptimizedTaskController()
    counts = Counter()

    for i in range(n):
        task = Task(
            text=f"task-{i}",
            worth=rng.random(),
            novelty=rng.random(),
            urgency=rng.random(),
            complexity=rng.random(),
            redundancy=rng.random(),
            risk=rng.random() * 0.45,
            irreversible=rng.random() < 0.01,
        )
        counts[controller.decide(task).decision.value] += 1
    return counts
