# Routing Logic

The controller emits one of six decisions:

- `CACHE`
- `SMALL_MODEL`
- `FRONTIER_MODEL`
- `BATCH`
- `DROP`
- `HUMAN`

Priority:
1. Human gate for irreversible/high-risk work.
2. Cache gate for highly redundant work.
3. Drop gate for low-value non-urgent work.
4. Batch gate for valuable but non-urgent work.
5. Frontier route for high complexity/value.
6. Small model for the remaining useful tasks.

Thresholds are configurable in `config/controller.json`.
