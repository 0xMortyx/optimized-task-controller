# Architecture

Optimized Task Controller sits between task producers and execution backends.

```text
Users / Agents / Webhooks / Cron / Apps
                  │
                  ▼
          Task Normalization
                  │
                  ▼
        ┌───────────────────┐
        │  Task Controller  │
        └───────────────────┘
          │   │   │   │
          │   │   │   └──────────→ HUMAN
          │   │   └──────────────→ BATCH
          │   └──────────────────→ CACHE / DROP
          └──────────────────────→ MODEL ROUTER
                                      │
                               ┌──────┴──────┐
                               ▼             ▼
                         SMALL MODEL   FRONTIER MODEL
```

Stages:
1. Normalize task metadata.
2. Check irreversible/high-risk flags.
3. Check cached/redundant work.
4. Score urgency, novelty, worth and complexity.
5. Decide whether the task can wait.
6. Pick the cheapest capable tier.
7. Emit a routing receipt.
