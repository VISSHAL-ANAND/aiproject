# Agent Instructions (Tier 1)

Always read `DOX/docs/STATE.md` first, then only the next actionable item in `DOX/docs/TASKS.md`. Read PRD/TRD/FLOW when relevant.

- Never claim an index is calibrated accident probability without calibration and prospective/time-geographic validation.
- Never fabricate datasets, live traffic, metrics, or test results.
- Keep provider failures graceful and missing/stale inputs visible.
- Keep secrets out of source control; commit only `.env.example`, never `.env`.
- Add/update tests for behavior changes and run `python -m pytest`.
- Record major decisions and update STATE/TASKS after meaningful work.
- Respect dataset licenses, API terms, attribution, rate limits, and privacy.
