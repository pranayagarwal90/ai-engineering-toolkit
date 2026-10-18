---
name: site-outage-investigation
description: Diagnose site unavailability across relevant request, infrastructure, Drupal, cache, database, storage, or external-service boundaries without exhaustive scanning or automatic remediation.
---

# Investigate site availability

Follow [shared rules](../../RULES.md), the [project map](../../project/README.md) and [operations](../../project/operations.md).

**Scope:** a request to investigate is read-only. Do not restart services, flush Redis/cache, change DNS, deploy, import config, restore databases or disable security as automatic diagnosis.

## Inputs

- Environment, incident window and timezone, affected URL, reach (one feature or the whole site), observed status or timeout, recent changes.

## Steps

1. **Choose the next boundary from the symptom.** Do not run every row as a checklist:

   | Evidence | Next useful boundary |
   | --- | --- |
   | Name resolution/TLS failure before any HTTP response | Client/DNS/CDN/proxy evidence supplied by the operator; topology is not established by this repo. |
   | Public URL fails but a verified origin succeeds | Proxy/CDN/tunnel/routing/TLS evidence. Test each edge or relay separately when there are several; one healthy path can hide a broken one. |
   | Gateway error, unhealthy/missing container, origin timeout | Web server/PHP/container state and bounded logs; verify the actual service name from the runbook/environment. |
   | Drupal/PHP exception or one failing route | [drupal-log-analysis](../drupal-log-analysis/SKILL.md) to correlate logs, stack frames, code and changes. |
   | Bootstrap or connection failure | The settings mount, database or Redis reachability/state the error points to; no repeated dblog requests when bootstrap cannot complete. |
   | Read-only filesystem, write failure, capacity error | The affected path/mount, permissions or storage capacity, without dumping files or recursively changing permissions. |
   | Only one external integration fails | That integration and its failure/fallback behavior, using the integrations map. |
   | Site works but shows old behavior after a release | The running revision versus the intended one ([pinned image deployment](../pinned-image-deployment/SKILL.md)), before debugging code. |

2. **Collect bounded evidence.**
   - Use commands verified in operations or the tool's own help. Verify commands for DNS, proxies and external hosts before use; mark missing access unknown.
   - Preserve current symptoms and logs before considering changes.
   - Compare public and origin behavior only with a confirmed origin and permitted read-only checks. Do not bypass access controls or expose private endpoints.
3. **Classify and stop at the evidence gap.**
   - Mark findings **verified failure**, **suspected failure** or **unavailable evidence**; keep a short timeline separating the first supported failure from cascading symptoms.
   - Stop expanding when the next test needs access you do not have; name that gap instead of scanning other layers speculatively.
4. **Remediate only when asked.** Propose the evidence-backed minimal action, rollback impact and environment-specific verification, then act only within that authorization.

## Output

Reuse the log-analysis incident report where it applies, and add the affected layer, blast radius, next discriminating check and recovery criteria. A single successful homepage response does not prove every affected function recovered.
