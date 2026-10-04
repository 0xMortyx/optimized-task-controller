from src.optimized_task_controller import OptimizedTaskController, Task

controller = OptimizedTaskController()
task = Task(
    text="Analyze this week's deployment incidents and summarize the root causes.",
    worth=0.8,
    novelty=0.7,
    urgency=0.6,
    complexity=0.65,
)
print(controller.decide(task))
