# OpenCode Agent Evaluation Results

Do not place real transcripts, user code, secrets, or proprietary content here.
Keep raw material in ignored `results/raw/`; use neutral run IDs in scorer copies.

## Run configuration

- Fixture revision / Git commit:
- OpenCode version:
- Model and exact version:
- Provider:
- Sampling parameters:
- Tool permissions:
- Operator:
- Scorer and blinding method:
- Start/end date:
- OpenCode package deployment verification (B only):
- Deviations / unavailable fields:

## Individual runs

Copy one row per execution, including invalid/repeated executions. Metric source
must be recorded; use `N/A` when not exposed.

| Run ID | Task | Rep | Condition (sealed until scoring) | Order | Status / invalid reason | Agent | Model/config match | Input tokens + source | Output tokens + source | Cost + source | Latency + source | Loaded context observed | Retries / interruptions / deviations | Score 0–4 | Critical failure + evidence | Commands and exit codes |
|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|---:|---|---|
| | | | | | | | | | | | | | | | | |

## Locked blind scores

Complete before revealing the condition mapping.

| Run ID | Task | Score | Critical failure? | Evidence / rubric items |
|---|---|---:|---|---|
| | | | | |

## Paired comparison

Report each repetition and retain invalid attempts in the individual log.

| Task | Rep | A run ID / score | B run ID / score | Quality delta (B-A) | A cost | B cost | Cost delta / unavailable | Valid pair? |
|---|---:|---|---|---:|---|---|---|---|
| | | | | | | | | |

## Summary and decision

| Persona | Valid pairs | Quality median/range A | Quality median/range B | Cost median/range A | Cost median/range B | Critical failures |
|---|---:|---|---|---|---|---|
| rust-dev | | | | | | |
| rust-reviewer | | | | | | |
| rust-tester | | | | | | |

- Overall decision: favorable signal / inconclusive / no gain
- Quality-first rationale:
- Consistency of measured cost change:
- Latency observations:
- Context/loading observations (do not infer from installed files):
- Limitations and protocol deviations:
- Proposed next round:
