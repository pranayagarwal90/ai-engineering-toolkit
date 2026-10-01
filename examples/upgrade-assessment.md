# Illustrative upgrade assessment

Status: fictional exercise, not a real project result.

Request: “Assess whether drupal/example_extension can move from its locked version to the target release I provide. Do not apply changes.”

Read the maintenance profile and upgrade-assessment skill. Inputs include a manifest constraint, lockfile version, PHP/core declarations and official target release metadata.

Expected report: compare declared/locked/installed/deployed versions separately; identify compatibility blockers and affected custom code; propose a bounded update and verification plan. If target metadata cannot be accessed, mark it unknown. Do not invent versions or run a real update.

Acceptance checks: manifest/lock are unchanged; each compatibility claim has evidence; no production safety or successful tests are asserted without observations.
