# Report inputs

Supply sanitized report excerpts or supported exports with relevant source. No specific JSON export format is required.

| Evidence | Purpose |
| --- | --- |
| Product/version, language and analyzer | Interpret terminology and rule behavior |
| Analysis time, revision, branch/PR | Match findings to source |
| Gate conditions, comparator, thresholds and values | Explain why the gate failed |
| New-code definition and scope | Distinguish current change from existing debt |
| Rule key, message, location and flow | Reconstruct the reported failure path |
| Hotspot category and review status | Guide contextual security review |
| Coverage import/build output | Distinguish missing evidence from low tested coverage |

If using an existing authorized API integration, inspect that instance's documented API and handle pagination; do not invent endpoints or assume issues and hotspots share an API. This toolkit contains no network integration.

Official sources, checked during authoring on 2026-10-01:
- [SonarQube Server quality gates](https://docs.sonarsource.com/sonarqube-server/2026.1/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates)
- [SonarQube Server security hotspots](https://docs.sonarsource.com/sonarqube-server/2026.1/user-guide/security-hotspots)
- [SonarQube Cloud quality gates](https://docs.sonarsource.com/sonarqube-cloud/standards/managing-quality-gates/introduction-to-quality-gates)

A hotspot highlights security-sensitive code needing review; review can establish that no fix is needed or that a fix is required. Gates use conditions on analysis measures; use the actual project policy rather than copying a documented default.
