# Manual Protocol

## Conditions

- **A, baseline:** clean fixture, no package agents, skills, rules, or
  instructions. Use the same short neutral prompt preamble for every A run:
  “Work only in this Rust fixture. Follow the task prompt, inspect relevant
  files, and report exact commands and outcomes. Do not claim commands you did
  not run.”
- **B, treatment:** fresh reset, then deploy with
  `./sync.sh opencode evaluation/opencode/fixture/work`. Use the same preamble
  plus the task prompt and select the named persona (`rust-dev`,
  `rust-reviewer`, or `rust-tester`). Do not manually add rules or skills.
Both conditions use the same repository snapshot, task prompt, model/version,
provider, sampling parameters, permissions, and initial user-visible context,
except for the installed package and persona selection inherent to B. Use a new
session and fixture copy for each run.

## Automated execution and run order

There are six tasks and two paired repetitions per task (24 runs total). The
runner shuffles A/B order within each task/repetition using a recorded seed and
executes runs sequentially. Every invocation is a separate
`opencode --standalone run` session; no shared background server, conversation,
or changed fixture state is reused. It uses the official OpenCode CLI, not a
provider SDK or direct API call. Review the plan
with `--dry-run` first; the live run may incur provider charges.

Outputs receive neutral IDs. The raw output and condition mapping are local and
ignored by Git. Scorer-facing response copies should omit the mapping and
provider/session metadata; content may still reveal the treatment indirectly,
so describe blinding as partial unless an independent scorer confirms otherwise.
Lock scores and critical-failure flags before opening the condition map.

## Fresh state and deployment checks

Run the no-provider `--preflight` first. It creates independent A/B copies,
checks the server's logged project root, confirms each B persona is resolved,
and requires the intentionally invalid model to be rejected. Do not start
provider-backed tasks if any preflight row fails.

Next run only `DEV-1` with one repetition as a paired smoke test. If both runs
are valid and scoped to their project roots, retain them as the first measured
pair and run the remaining 22 sessions with `--skip-pair DEV-1:1`. The runner
records the project root in each run and aborts immediately on invalid scope or
agent discovery rather than consuming the rest of the batch.

The runner creates a fresh copy of `fixture/initial` before each run. Before
each run it:

1. Confirms the copy contains only the fixture and fixed benchmark permission
   config, then initializes a local Git repository so OpenCode resolves that
   exact copy as the project root rather than inheriting the caller checkout.
2. For A, confirms the package `.opencode` directory does not exist.
3. For B, deploys using `./sync.sh opencode <run-project>` and confirms the
   expected `.opencode/agents`, `.opencode/rules`, `.opencode/skills`, and
   `.opencode/AGENTS.md` exist. Installed files are not evidence that any
   particular rule or skill was loaded during a session.
4. Invokes `opencode --standalone run --model <same-model> --format json` with the exact
   machine-readable prompt in `tasks.json`; B additionally selects the persona.
   No `--auto` permission bypass is used.

Do not edit package artifacts during the pilot. Keep real transcripts and
project-derived content under the ignored `results/raw/` directory, not in
versioned files. Use anonymous/synthetic excerpts only if publishing examples.

## Capture and validity

For each run record model/provider/version, parameters, selected agent, start
and end timestamps, observed CLI wall time, input/output tokens and monetary
cost with their source. The runner captures raw OpenCode JSONL and elapsed time;
parse token/cost fields only if present and attributable to the run. Mark
unavailable fields `N/A`; never infer token use, cost, or loaded context from
response length or installed files. Record observable loaded agent/skill/rule
identifiers and context volume, if exposed. Also record retries, interruptions,
context deviations, tool failures, and protocol deviations. The fixture
permission config is identical in every condition, denies external-directory access,
and allows only project tools plus Cargo shell commands.

Runs with a wrong fixture, inherited context, setup error, or materially changed
configuration are invalid. Preserve their log and reason, then repeat with a
new ID and fresh state; do not silently delete or replace them. Keep the failed
run in the results record.

For implementation/test tasks use only these fixed checks from each run's
project: `cargo fmt --check`, `cargo test`, and `cargo clippy -- -D warnings`.
Run all three after capture; record exact command and exit status.
For review tasks, compare findings manually to the task-specific answer key and
record missed seeded defects, false positives, and unsupported claims. Do not
score a reported gate as run unless independently observed in the run log.

## Scoring and decision

Score each output from 0 to 4 using only the task's observable rubric. Mark
critical failures separately. Preserve each run's score; compare paired A/B
results per task and summarize by persona using median, observed range, and
number of valid pairs. Report individual differences, unavailable metrics, and
all invalid/repeated runs. Quality is considered first: any critical failure
or lower treatment quality blocks a positive efficiency conclusion. A
favorable signal requires no quality regression and consistently lower
measurable cost on relevant tasks. Otherwise conclude “inconclusive/no gain.”
Do not generalize beyond this fixture, model/configuration, and OpenCode setup.
