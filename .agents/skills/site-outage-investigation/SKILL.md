---
name: site-outage-investigation
description: Diagnose site unavailability across relevant request, infrastructure, Drupal, cache, database, storage, or external-service boundaries without exhaustive scanning or automatic remediation.
---

# Investigate site availability

Follow [root guidance](../../../AGENTS.md), the [architecture map](../../../architecture/README.md), and [operations](../../../architecture/operations.md). Establish environment, incident window/timezone, affected URL, reach (one feature versus whole site), observed status/timeout and recent changes. Treat a request to investigate as read-only.

Use symptoms to choose the next boundary; do not run every row as a checklist:

| Evidence | Next useful boundary |
| --- | --- |
| Name resolution/TLS failure before any HTTP response | Client/DNS/CDN/proxy evidence supplied by the operator; topology is not established by this repo. |
| Public URL fails but a verified origin succeeds | Proxy/CDN/routing/TLS evidence; this does not by itself identify the defective component. |
| Gateway error, unhealthy/missing container, origin timeout | Web server/PHP/container state and bounded logs; verify the actual service name from the runbook/environment. |
| Drupal/PHP exception or one failing route | Use [drupal-log-analysis](../drupal-log-analysis/SKILL.md) to correlate logs, stack frames, code and changes. |
| Bootstrap or connection failure | Relevant settings mount, database or Redis reachability/state indicated by the error; no repeated dblog requests when bootstrap cannot complete. |
| Read-only filesystem, write failure, capacity error | Affected path/mount, permissions or storage capacity evidence, without dumping files or recursively changing permissions. |
| Only one external integration fails | The specific external integration and its failure/fallback behavior, using the integrations map. |

Collect bounded evidence with commands verified in operations or the current tool's help. Commands for DNS/proxies/external hosts not established here must be verified before use; mark absent access unknown. Preserve current symptoms/logs before considering changes. Compare public versus origin behavior only with a confirmed origin/host and permitted read-only checks; do not bypass access controls or expose private endpoints.

Classify findings as **verified failure**, **suspected failure**, or **unavailable evidence**. Maintain a short timeline and distinguish the first supported failure from cascading symptoms. Stop expanding when the next test needs unavailable infrastructure access; identify that specific gap rather than speculatively scanning other layers.

Do not restart services, flush Redis/cache, change DNS, deploy, import config, restore databases, or disable security as automatic diagnosis. If remediation is explicitly requested, propose the evidence-backed minimal action, rollback impact and environment-specific verification, then proceed only within that authorization. Reuse the log-analysis incident report when applicable and add affected layer, blast radius, next discriminating check, and recovery criteria. A single successful homepage response is not proof that all affected functions recovered.
