# Behavior evaluation cases

The validator proves the files are well-formed. These cases check something different: whether a skill changes what an assistant actually does. Each case is a fixed task with supplied evidence and a scoring rubric. Most are taken from a real incident recorded in [examples](../examples/).

## Results

| Date | Client and model | Baseline | With skill | Write-up |
| --- | --- | --- | --- | --- |
| 2026-10-18 | Claude Code CLI, claude-opus-5-5 | 1/5 passed, 22/32 points, 2 violations | 5/5 passed, 29/32 points, 0 violations | [results](results/2026-10-18-claude-opus-5-5.md) |

These are single runs, graded by the same model and written by the skills' author. The write-up lists the limits; treat them as a first signal.

## Running the cases automatically (Claude Code)

```bash
python3 evals/run_claude.py --model <model> [--claude /path/to/claude] [--case <id> ...]
```

For each case, [run_claude.py](run_claude.py) asks the question twice in throwaway directories:
- **baseline:** no tools, only the Task and Evidence
- **with skill:** the skill installed by `scripts/install.py`, with Read as the only tool

A separate blind run then grades both answers against the rubric, shown as A and B in random order. Raw answers, grades and `summary.json` go to `results/runs/<date>-<model>/`. Run it from outside any project that has its own `CLAUDE.md` or `AGENTS.md`, and check the grades by hand before publishing them.

## Running a case by hand

1. Use a scratch directory containing nothing but the case's evidence. No access to real systems is needed, and none should be granted.
2. **Baseline run:** give the assistant the **Task** and **Evidence** only.
3. **Skill run:** in a fresh session, give the same input plus "Read .agents/RULES.md and `<skill path>`" with this repository available.
4. Score both answers against the **Rubric**:
   - Each **Must** item met earns its points.
   - Any **Must not** item violated fails the run, whatever the score.
5. Record both runs from [results/TEMPLATE.md](results/TEMPLATE.md) as `results/<case-id>-<client>-<date>.md`, with the client, model and version used.

Score from what the answer says and proposes. If the assistant could act, an attempted forbidden action counts as a violation, even if a guard stopped it.

## Cases

| Case | Skill | From |
| --- | --- | --- |
| [config-import-unexplained-update](cases/config-import-unexplained-update.md) | drupal-config-drift | [real incident](../examples/unexpected-config-import.md) |
| [check-for-newer-image](cases/check-for-newer-image.md) | pinned-image-deployment | real task |
| [deploy-reported-success](cases/deploy-reported-success.md) | pinned-image-deployment | [real incident](../examples/deploy-reported-success.md) |
| [public-url-one-relay-down](cases/public-url-one-relay-down.md) | homelab-health-triage | [real incident](../examples/public-url-one-relay-down.md) |
| [mixed-image-updates](cases/mixed-image-updates.md) | container-image-updates | synthetic |

## Adding a case

- Base it on a concrete task. Supply only sanitized evidence.
- Make every rubric item observable in the answer. "Mentions X" or "does not propose Y" can be scored; "understands X" cannot.
- Include at least one **Must not** item for the unsafe shortcut an assistant is likely to take.
- The validator checks each case's frontmatter, sections and skill path.
