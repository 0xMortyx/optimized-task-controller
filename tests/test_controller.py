from src.optimized_task_controller import OptimizedTaskController, Task
from src.optimized_task_controller.models import Decision

def test_irreversible_goes_to_human():
    assert OptimizedTaskController().decide(Task("delete production database", irreversible=True)).decision == Decision.HUMAN

def test_redundant_goes_to_cache():
    assert OptimizedTaskController().decide(Task("known answer", redundancy=0.95)).decision == Decision.CACHE

def test_complex_goes_frontier():
    task = Task("complex reasoning", worth=0.9, novelty=0.9, urgency=0.8, complexity=0.95)
    assert OptimizedTaskController().decide(task).decision == Decision.FRONTIER_MODEL
