# Contributing

Open an issue using the workflow-problem or new-workflow template: describe the task, client/version, observed result and desired behavior. Use sanitized code, diffs and logs. Do not include credentials, internal hosts or personal data.

## Changes

- Keep one workflow concern per change, on a branch with a pull request; `main` should stay green, so do not land a collection one file at a time.
- Explain triggering conditions and verification.
- Run `python3 -m unittest discover -s tests` and `python3 scripts/validate_toolkit.py`. The validator needs no edits when you add files, but every skill, profile and prompt must be linked from `.github/AI-WORKFLOWS.md`.
- Record the change under **Unreleased** in the changelog.

## Writing a skill

- Frontmatter: `name` (lowercase-hyphenated, equal to the folder name) and a `description` that says when to use it.
- Structure: a short scope paragraph, then **Inputs**, **Steps** (one action per step, details as sub-bullets) and **Output**. Keep it skimmable; avoid single-paragraph steps.
- State evidence requirements and what the skill must not do without explicit scope.
- Add an illustrative or real-use example, labelled accurately, and preferably an [evaluation case](evals/README.md#adding-a-case) whose Must-not items cover the unsafe shortcut. Avoid automatic deployments, unsupported success claims and duplicate procedures.
