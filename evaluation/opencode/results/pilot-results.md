# OpenCode Pilot Results

## Scope and validity

- Fixture: `evaluation/opencode/fixture/initial`, isolated by a per-run Git root.
- OpenCode: `v2.3.2`.
- Model/provider: `openai/gpt-6-luna` / `openai`.
- Conditions: A default OpenCode agent without the package; B deployed OpenCode package and task persona.
- Valid sample: 24 sessions, 12 per condition; six tasks x two repetitions x A/B.
- All 24 session logs confirmed their own fixture as the OpenCode project root. All treatment personas were found.
- Earlier attempts with incorrect project roots or missing personas are preserved under ignored `results/raw/` and excluded here.
- Sampling settings used OpenCode defaults; no per-run override was supplied.

This is an exploratory pilot, not a blinded or statistically powered evaluation. The operator knew the A/B mapping while reviewing outputs. Scores below apply the task rubrics but must not be interpreted as independently blind-scored.

## Rubric scores

Scores are 0-4 per run. Pair totals are the sum of two repetitions, out of 8.

| Task | A rep 1 | A rep 2 | A total | B rep 1 | B rep 2 | B total |
|---|---:|---:|---:|---:|---:|---:|
| DEV-1 | 4 | 4 | 8/8 | 4 | 3 | 7/8 |
| DEV-2 | 4 | 4 | 8/8 | 4 | 4 | 8/8 |
| REV-1 | 4 | 4 | 8/8 | 4 | 4 | 8/8 |
| REV-2 | 4 | 4 | 8/8 | 4 | 4 | 8/8 |
| TEST-1 | 4 | 4 | 8/8 | 4 | 4 | 8/8 |
| TEST-2 | 4 | 4 | 8/8 | 4 | 4 | 8/8 |
| **Total** | **24/24** | **24/24** | **48/48** | **24/24** | **23/24** | **47/48** |

One critical failure occurred in B, DEV-1 repetition 2: `checked_mean` uses an `i64` accumulator. On a 64-bit target, an addressable slice with more than roughly 4.3 billion `i32::MAX` values can overflow `i64`, violating the prompt's no-overflow contract. The tests cover `i32` overflow but not `i64` overflow. A used `i128`; B repetition 1 used `f64`. In both conditions, implementation tasks otherwise fixed the seeded behavior and added the requested tests. Test-only tasks left production code unchanged and their focused regressions failed on the intended buggy fixture. Both reviewers identified their seeded target. REV-2 B repetition 2 additionally overstated the unconstrained lifetime as inherently unsound; the missing unsafe contract finding was valid, but the lifetime claim alone should not be treated as a defect for an `unsafe` API whose caller must uphold its safety contract. Other unrelated review findings were not included in the task scores.

## Verification

- DEV tasks: all `cargo test` and `cargo clippy -- -D warnings` checks passed. One `cargo fmt --check` failed: DEV-1 repetition 2 in A had a formatting difference in an assertion. The other DEV formatting checks passed.
- TEST-1: all four focused `cargo test first_max_index` checks failed on the seeded repeated-maximum defect, as expected; three boundary cases passed in each run. Formatting and Clippy passed.
- TEST-2: all four focused overflow regression checks failed with overflow panic on the seeded `.sum()` implementation, as expected; formatting and Clippy passed.
- Reviewer sessions were not assigned automated gates. Claims of validation in their responses were checked against captured command events; the observed claims matched those events.

Expected failing regression tests are evidence that the seeded bug was detected, not failed benchmark sessions.

## Efficiency observations

Token values are OpenCode `step_finish` fields. `input` and `cache_read` are reported separately and are not combined. Cost is OpenCode-reported cost, not a provider billing statement.

| Persona group | Condition | Sessions | Median latency (s) | Input tokens | Cache-read tokens | Output tokens | OpenCode-reported cost |
|---|---|---:|---:|---:|---:|---:|---:|
| All | A | 12 | 20.67 | 107,062 | 218,880 | 5,832 | 0.00 |
| All | B | 12 | 24.86 | 132,450 | 273,536 | 6,601 | 0.00 |
| rust-dev | A | 4 | 18.91 | 45,660 | 115,840 | 2,027 | 0.00 |
| rust-dev | B | 4 | 27.40 | 35,150 | 98,048 | 2,396 | 0.00 |
| rust-reviewer | A | 4 | 22.97 | 40,794 | 52,864 | 2,267 | 0.00 |
| rust-reviewer | B | 4 | 27.07 | 69,622 | 91,776 | 2,762 | 0.00 |
| rust-tester | A | 4 | 20.67 | 20,608 | 50,176 | 1,538 | 0.00 |
| rust-tester | B | 4 | 21.00 | 27,678 | 83,712 | 1,443 | 0.00 |

## Conclusion and limitations

- Rubric scores were A 48/48 and B 47/48; scoring was manual and unblinded.
- B had higher aggregate reported input (+23.7%), cache-read (+25.0%), output (+13.2%), and median latency (+20.3%) than A. Variation between tasks and repetitions is substantial at this sample size.
- OpenCode reported cost `0.00` for every valid run. This does not prove that the provider billed zero; consult the provider account's usage/billing view for actual charges.
- The critical correctness failure blocks a positive efficiency conclusion for B. B also used more reported tokens and had higher median latency in this fixture/configuration. Do not generalize to other projects, models, providers, or targets.
- Raw transcripts, private condition maps, and per-run projects remain local under the Git-ignored `results/raw/` directory.
