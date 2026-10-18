---
name: drupal-security-update
description: Determine Drupal advisory applicability and the smallest supported dependency remediation; apply it only when implementation is explicitly requested.
---

# Assess and remediate a security advisory

Follow [shared rules](../../RULES.md), the [project map](../../project/README.md) and the relevant security/maintenance pages.

**Scope:** keep advisory assessment separate from implementation. Do not disable security controls, suppress audit findings or widen constraints to produce a passing result. Do not claim a production issue is fixed until deployment and production verification are separately evidenced.

## Inputs

- Advisory URL or package, environment, and whether assessment or implementation is requested.

## Steps

1. **Read the advisory from current sources.**
   - Advisory/CVE, authoritative Drupal/project/vendor URL, publication/update date, affected package and range, fixed versions, exposure conditions.
   - Do not rely on remembered version ranges. If sources are blocked, label applicability and patch status provisional.
2. **Decide applicability with evidence.**
   - Compare `composer.json`, `composer.lock`, installed metadata and deployed-version evidence.
   - A vulnerable locked package is not proven deployed exposure; disabled functionality does not necessarily remove vulnerable code. Record affected, unaffected or unresolved.
3. **Pick the smallest patched target.**
   - Inspect constraints, PHP/Drupal requirements and transitive dependencies using [upgrade assessment](../drupal-upgrade-assessment/SKILL.md).
   - Smallest vendor-supported target that addresses the relevant advisories; never update every dependency by default. Check related advisories for an incomplete fix.
4. **Propose the remediation.**
   - Exact bounded change, required local hooks/cache/config work, regression checks and rollback limits.
   - If only assessment was requested, report now without changing dependencies.
5. **Implement only when requested.**
   - Carry the assessment into [core update](../drupal-core-update/SKILL.md) or [contrib update](../drupal-contrib-update/SKILL.md). These are procedures, not automatic agent handoffs.
   - For other transitive packages, keep the same bounded principles and explain why the owning dependency must change.
6. **Verify.**
   - The exact CI audit in [maintenance](../../project/maintenance.md), the shared quality gate, relevant security regressions and local behavior checks.
   - Compare remaining findings with the original advisory; distinguish an audit network failure from a clean result.

## Output

Advisory/package evidence, repository and deployment applicability, the selected safe target, constraint/dependency impact, remediation performed or proposed, database/cache/config status, checks and remaining vulnerabilities/unknowns. If no supported compatible fix exists, explain the blocker and escalation options without an unrequested major upgrade. Keep any rollback-to-vulnerable-version risk explicit.
