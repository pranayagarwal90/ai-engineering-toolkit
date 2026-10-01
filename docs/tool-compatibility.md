# Tool compatibility

The portable baseline is explicit file reading: ask your assistant to read AGENTS.md, the selected SKILL.md and relevant project references.

| Client | Entry point |
| --- | --- |
| Claude Code | CLAUDE.md imports AGENTS.md; explicitly request the skill by path when discovery is unavailable |
| Codex | Use repository guidance and explicitly provide the skill path; verify discovery in your installed client |
| GitHub Copilot / VS Code | Profiles and prompt files are supplied; verify availability and supported frontmatter in your installed version; fall back to explicit paths |

Automatic discovery varies by client version, workspace and session mode. Profiles inherit available tools; they do not install runtimes or schedule work. There are no automatic agent handoffs.

Official references: [Claude memory](https://code.claude.com/docs/en/memory), [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex skills](https://developers.openai.com/codex/skills), [VS Code agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents), [VS Code prompts](https://code.visualstudio.com/docs/copilot/customization/prompt-files).

Public edition validation covers structure and links, not execution across all these clients.
