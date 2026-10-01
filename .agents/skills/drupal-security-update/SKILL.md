---
name: drupal-security-update
description: Determine Drupal advisory applicability and the smallest supported dependency remediation; apply it only when implementation is explicitly requested.
---

# Assess and remediate a security advisory

Follow [root guidance](../../../AGENTS.md), the [architecture map](../../../architecture/README.md), and the relevant security/maintenance pages. Keep advisory assessment separate from implementation.

1. Identify the advisory/CVE, authoritative Drupal/project/vendor URL, publication/update date, affected package/range, fixed versions and relevant exposure conditions. Verify current sources; do not rely on remembered version ranges. If source access is blocked, label applicability/patch status provisional.
2. Compare `composer.json`, `composer.lock`, installed metadata and any deployed-version evidence. Distinguish a vulnerable locked package from proven deployed exposure; disabled functionality does not necessarily remove vulnerable code. Record affected, unaffected, or unresolved with evidence.
3. Inspect constraints, PHP/Drupal requirements and transitive dependencies using [upgrade assessment](../drupal-upgrade-assessment/SKILL.md). Select the smallest vendor-supported patched target that addresses the relevant advisories; never default to updating every dependency. Check related advisories for an incomplete fix.
4. Propose the exact bounded remediation, required local hooks/cache/config work, regression checks, and rollback limits. If only a review/assessment was requested, report now without changing dependencies. Do not disable security controls, suppress audit findings or widen constraints merely to produce a passing result.
5. When implementation is explicitly requested, carry the assessment into [core update](../drupal-core-update/SKILL.md) or [contrib update](../drupal-contrib-update/SKILL.md) as appropriate. These files are procedural references, not automatic agent handoffs. For other transitive packages, keep the same bounded Composer/verification principles and explain why the owning dependency must change.
6. Run the exact CI audit in [maintenance](../../../architecture/maintenance.md), the shared quality gate, relevant security regressions and local behavior checks after remediation. Compare remaining findings to the original advisory; distinguish audit-network failure from a clean result. Do not claim the production issue is fixed until deployment and production verification are separately evidenced.

Return advisory/package evidence, repository/deployment applicability, selected safe target, constraint/dependency impact, remediation performed or proposed, database/cache/config status, checks and remaining vulnerabilities/unknowns. If no supported compatible fix is available, explain the blocker and escalation options without performing an unrequested major upgrade. Keep any rollback-to-vulnerable-version risk explicit.
