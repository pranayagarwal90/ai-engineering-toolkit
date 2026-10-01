# SonarQube gate failure: fix the defect, investigate the coverage

Status: realistic illustrative exercise. All findings, values and snippets are synthetic; no scanner or server was run for this example.

## Problem

A PHP pull request builds successfully, but its SonarQube quality gate fails. The developer sees a possible null dereference and unexpectedly low new-code coverage. A security hotspot also needs review. Treat these as distinct questions rather than one generic “Sonar failure.”

Sample project policy (not Sonar defaults):

| Condition | Observed | Required | Result |
| --- | --- | --- | --- |
| New-code reliability issues | 1 | 0 | Failed |
| New-code coverage | 42% | At least 80% | Failed |
| New security hotspots reviewed | 0% | 100% | Failed |

The report revision must match the source being inspected. Rule keys, analyzer versions and actual gate conditions would be supplied by the user in a real task.

## Sample source

```php
$account = $this->accountRepository->find($account_id);
return $account->getDisplayName();
```

The repository's documented contract allows find() to return null when no account exists. If that contract is verified, the dereference can fail. The report alone does not prove this contract.

## Copyable analysis prompt

> Read AGENTS.md and .agents/skills/sonarqube-analysis/SKILL.md.
> Analyze this PHP report and the matching source revision. Explain each
> failing gate condition separately. Trace the possible null dereference,
> check whether coverage data imported correctly, and identify evidence
> needed to review the hotspot. Do not change code or SonarQube settings.

Use the [Code Quality Analyst](../.github/agents/code-quality-analyst.agent.md) and [analysis prompt](../.github/prompts/analyze-sonarqube-report.prompt.md). Supply the real report and helper implementation alongside this request.

## Expected investigation

- Confirm the lookup contract and whether the absent-account path is reachable.
- Decide the intended behavior for a missing account with the caller/business contract. Do not invent a fallback or change access behavior.
- Check test output, coverage artifact generation/import and source-path matching before concluding the suite genuinely covers only 42% of new code.
- Inspect the hotspot's actual rule, location, input flow and security context. A hotspot might be safe or require a fix; it is not automatically a vulnerability.

## Conditional remediation

If missing accounts should produce an empty display value according to the existing contract:

```php
$account = $this->accountRepository->find($account_id);
if ($account === NULL) {
  return '';
}
return $account->getDisplayName();
```

Use the runtime and coding conventions of the target project. If the application should return a domain error or not-found response instead, implement that established behavior. Do not use an empty string merely to silence the analyzer.

Request: “Apply the supported null-handling fix locally. Add or run appropriate tests for absent and existing accounts. Correct coverage-import configuration only if evidence proves it is wrong. Preserve the quality gate. Do not scan a server or change issue statuses.”

## Verification and acceptance

| Check | Evidence to record |
| --- | --- |
| Absent account | Agreed behavior, no null dereference |
| Existing account | Original display value preserved |
| Access/authorization | Existing policy unchanged |
| Coverage | Report generated and imported for intended files/revision |
| Hotspot | Contextual review rationale; authorized human/server review |
| Reanalysis | Completed scan on matching branch/revision; actual condition results |

These checks are planned, not executed here. Local tests alone cannot establish that SonarQube resolved a finding or passed the gate. If no server integration is available, report those results as unverified.

Do not remove code from coverage, mark hotspots safe without review, add NOSONAR or lower thresholds to obtain a pass.
