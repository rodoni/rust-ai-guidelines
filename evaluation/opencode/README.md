# OpenCode Agent Evaluation Pilot

This isolated benchmark compares minimal OpenCode instructions (A) with the
installed guideline package (B). The earlier compact-agent experiment was
rejected after critical review misses; its report remains for history, but the
variant has been removed. No compact instructions are active in production.

## Contents

- `fixture/`: the versioned Rust project used in every run.
- `tasks.md`: six fixed tasks, prompts, expected outcomes, scoring rubrics, and
  reviewer answer key. Keep the key hidden from the quality scorer until scores
  are locked.
- `protocol.md`: setup, randomization, blinding, capture, and decision procedure.
- `tasks.json`: machine-readable prompts matching the rubric IDs in `tasks.md`.
- `run.py`: sequential orchestration through the official OpenCode CLI.
- `results/template.md`: one record per run and paired summary template.
- `reset.sh`: recreate `fixture/work` from the pristine `fixture/initial` tree.

The runner makes an independent fixture copy for each execution. First verify
that OpenCode stays inside each copy and can discover all three personas. The
preflight uses an intentionally invalid model ID and must fail before a
provider request:

```sh
python3 evaluation/opencode/run.py --model openai/gpt-6-luna --preflight
```

Then preview the 24 planned A/B sessions without model calls:

```sh
python3 evaluation/opencode/run.py --model openai/gpt-6-luna --dry-run
```

For staged execution, start with one A/B pair (two provider-backed runs):

```sh
python3 evaluation/opencode/run.py --model openai/gpt-6-luna --task DEV-1 --repetitions 1 --execute
```

If that pair is valid, use it as `DEV-1` repetition 1 and execute the other 22
runs with `--skip-pair DEV-1:1 --execute`. The runner aborts after an invalid
session and checks the logged project root on every run.

Keep real outputs under `results/raw/`; that directory is ignored by Git.

The runner does not call a provider API directly and does not use parallel calls.
It invokes `opencode --standalone run` once per run to avoid sharing a server
location with the caller checkout, and records the raw CLI stream, elapsed time,
and condition map locally. Cost and token metrics are only included when
exposed by OpenCode. Run `./sync.sh verify` separately for repository integrity.
