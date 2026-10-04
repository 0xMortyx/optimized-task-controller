# Optimized Task Controller

> A decision layer that sits in front of the queue.

**Optimized Task Controller (OTC)** decides whether each task should be routed to a model, answered from cache, delayed into a batch, dropped, or escalated to a human.

Instead of sending every request straight to the most expensive model, OTC scores the request first.

```text
incoming task
    ↓
worth / novelty / risk / urgency / complexity
    ↓
┌─────────┬─────────┬─────────┬────────┬────────┬─────────┐
│  CACHE  │  SMALL  │ FRONTIER│  BATCH │  DROP  │  HUMAN  │
└─────────┴─────────┴─────────┴────────┴────────┴─────────┘
```

## The idea

Most tasks do not need the biggest model.

A 24/7 agent, a few humans, webhooks, automations, background jobs and user requests can generate thousands of tasks per day. Sending all of them to a frontier model is expensive and often unnecessary.

OTC adds a control layer between **work generation** and **model execution**.

Every task passes through a lightweight decision pipeline that:

- scores whether the answer is worth generating
- checks whether the information is already known
- estimates the cheapest capable model tier
- decides whether the task can wait for a batch
- flags irreversible or high-risk actions
- routes, delays, escalates, or drops the task

## Decision pipeline

```text
Task
  │
  ├─→ Worth score
  ├─→ Novelty check
  ├─→ Complexity estimate
  ├─→ Urgency score
  ├─→ Reversibility / risk gate
  └─→ Cache check
        │
        ▼
 Decision Engine
        │
        ├─ CACHE
        ├─ SMALL_MODEL
        ├─ FRONTIER_MODEL
        ├─ BATCH
        ├─ HUMAN
        └─ DROP
```

## Example workload

The repository includes a deterministic simulator for a mixed agent workload.

Example output:

```text
tasks processed        8,400
small model            54.8%
batched                 18.2%
cache hit               11.4%
frontier model           8.6%
dropped                  5.4%
human escalation         1.6%
```

These values are **example/demo workload settings**, not a claim about universal production performance.

## Quick start

Requires Python 3.10+.

```bash
python -m src.optimized_task_controller.cli --simulate 8400
```

Try a single task:

```bash
python -m src.optimized_task_controller.cli \
  --task "Summarize the latest deployment logs" \
  --urgency 0.7 \
  --novelty 0.4 \
  --complexity 0.3
```

## Core actions

| Decision | Meaning |
|---|---|
| `CACHE` | Answer already exists or can be reused |
| `SMALL_MODEL` | Cheapest capable model should handle it |
| `FRONTIER_MODEL` | High-value / high-complexity request |
| `BATCH` | Non-urgent work can wait and be processed together |
| `DROP` | Low-value or redundant work |
| `HUMAN` | Irreversible / high-risk action |

## Repository structure

```text
optimized-task-controller/
├── config/
│   └── controller.json
├── examples/
│   └── demo.py
├── src/
│   └── optimized_task_controller/
│       ├── __init__.py
│       ├── models.py
│       ├── scoring.py
│       ├── controller.py
│       ├── simulation.py
│       └── cli.py
├── tests/
│   └── test_controller.py
├── ARCHITECTURE.md
├── ROUTING.md
├── ROADMAP.md
├── pyproject.toml
└── README.md
```

## Why this layer matters

Model quality is only one part of an agent system.

At scale, the bigger problem becomes:

**Which tasks deserve inference at all?**

Routing, batching, caching and escalation can matter as much as the model itself.

## Roadmap

- [x] Rule-based decision engine
- [x] Cache / batch / drop / human routes
- [x] Model-tier selection
- [x] Workload simulator
- [ ] live queue adapters
- [ ] model/provider adapters
- [ ] latency + cost telemetry
- [ ] learned routing weights
- [ ] policy engine for irreversible actions
- [ ] feedback-based controller tuning

---

**Optimized Task Controller**

*The models were never the bottleneck. The routing was.*
