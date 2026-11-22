# Historical Compact-Agent Experiment

## Scope

- B: current installed package and source persona.
- C: same package, with only the selected persona replaced by its compact experimental version.
- Model/provider: `openai/gpt-6-luna`; OpenCode `v2.3.2`; OpenCode default sampling settings.
- Sample: six tasks, two repetitions, 12 valid sessions per condition. Every run verified its isolated project root and selected persona.
- Outputs were manually scored by the operator, who knew the condition. Scores are not independently or blindly evaluated.
- Raw output and private condition maps are retained under Git-ignored `results/raw/`.

## Quality

| Task | B current | C compact | Critical failure in C |
|---|---:|---:|---|
| DEV-1 | 8/8 | 8/8 | No |
| DEV-2 | 8/8 | 8/8 | No |
| REV-1 | 8/8 | 4/8 | Yes: repetition 2 missed the saturating-sum defect and stopped without reviewing the source |
| REV-2 | 8/8 | 4/8 | Yes: repetition 2 missed the seeded `raw_view` safety-contract defect |
| TEST-1 | 8/8 | 8/8 | No |
| TEST-2 | 8/8 | 8/8 | No |
| **Total** | **48/48** | **40/48** | **2 critical misses** |

The test-only tasks left production code unchanged and their seeded regression tests failed as expected in both conditions. The implementation tasks met the rubric in both conditions. One compact DEV-1 repetition had a `cargo fmt --check` failure; the remaining DEV/TEST formatting, compilation, and Clippy gates passed. Expected failures in TEST-1 and TEST-2 are not counted as benchmark failures.

The two compact review failures occurred despite correct project roots and persona discovery. In REV-1 repetition 2, the reviewer stopped after shell access to Git commands was denied instead of reading the source directly. In REV-2 repetition 2, it reported unrelated defects but missed the seeded unsafe API. The compact reviewer needs an explicit fallback to file-reading tools and stronger task-relevant defect checks; the current compact variant is not safe to promote.

## Efficiency

Token counts are OpenCode `step_finish` fields. Context tokens are calculated as `input + cache_read + cache_write`; cache fields remain separately visible. Cost is what OpenCode reported, not provider billing.

| Condition | Sessions | Median latency | Input tokens | Cache-read tokens | Output tokens | Context tokens | Reported cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| B current | 12 | 22.03 s | 137,267 | 299,520 | 7,448 | 436,787 | 0.00 |
| C compact | 12 | 22.15 s | 113,731 | 236,416 | 5,648 | 350,147 | 0.00 |

C used 19.8% fewer context tokens in aggregate, 24.2% fewer output tokens, and had essentially unchanged median latency (+0.5%). The median paired reduction in context tokens was only 5.9%, showing substantial task-to-task variation; the compact variant also regressed in reviewer quality. Observed skill loads were 20 for B (`rust-agentic-workflow` 10, `rust-testing` 6, `rust-resilience-app` 4) and 9 for C (`rust-testing` 6, `rust-api` 2, `rust-safety` 1). These counts are observations, not proof that skill selection alone caused the token difference.

OpenCode reported `0.00` cost for all sessions. This does not establish that the provider billed nothing.

## Decision

The compact variant is **rejected and discarded from the runnable evaluation source**: its aggregate context savings do not compensate for two critical review misses. No production agent was changed by this experiment. Compact prompt files were removed; per-run copies and transcripts remain locally under Git-ignored `results/raw/` as audit evidence. Scores are manual and unblinded, and two repetitions per task are not enough for broad statistical claims.
