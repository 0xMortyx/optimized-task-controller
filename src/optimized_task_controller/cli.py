import argparse
from .controller import OptimizedTaskController
from .models import Task
from .simulation import demo_distribution, organic_simulation

def pct(x, total):
    return (x / total * 100) if total else 0.0

def main():
    parser = argparse.ArgumentParser(description="Optimized Task Controller")
    parser.add_argument("--simulate", type=int, default=0)
    parser.add_argument("--organic", action="store_true")
    parser.add_argument("--task", default="")
    parser.add_argument("--worth", type=float, default=0.5)
    parser.add_argument("--novelty", type=float, default=0.5)
    parser.add_argument("--urgency", type=float, default=0.5)
    parser.add_argument("--complexity", type=float, default=0.5)
    parser.add_argument("--redundancy", type=float, default=0.0)
    parser.add_argument("--risk", type=float, default=0.0)
    parser.add_argument("--irreversible", action="store_true")
    args = parser.parse_args()

    if args.simulate:
        counts = organic_simulation(args.simulate) if args.organic else demo_distribution(args.simulate)
        print(f"tasks processed        {args.simulate:,}")
        for key in ["SMALL_MODEL", "BATCH", "CACHE", "FRONTIER_MODEL", "DROP", "HUMAN"]:
            print(f"{key.lower():20s} {pct(counts[key], args.simulate):5.1f}%")
        return

    controller = OptimizedTaskController()
    receipt = controller.decide(Task(
        text=args.task or "Summarize deployment logs",
        worth=args.worth,
        novelty=args.novelty,
        urgency=args.urgency,
        complexity=args.complexity,
        redundancy=args.redundancy,
        risk=args.risk,
        irreversible=args.irreversible,
    ))
    print("decision:", receipt.decision.value)
    print("score:", round(receipt.score, 3))
    print("reason:", receipt.reason)
    if receipt.model_tier:
        print("model_tier:", receipt.model_tier)

if __name__ == "__main__":
    main()
