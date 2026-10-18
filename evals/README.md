# Behavior evaluation cases

The validator proves the files are well-formed. These cases check something different: whether a skill changes what an assistant actually does. Each case is a fixed task with supplied evidence and a scoring rubric. Most are taken from a real incident recorded in [examples](../examples/).

No results are recorded yet. A case is only evidence once someone runs it and records the outcome.

## How to run a case

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
