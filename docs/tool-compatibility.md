# Tool compatibility

The toolkit is plain Markdown. Any assistant that can read files can use a skill when you name its path. `scripts/install.py` puts the files where each client looks for them.

| Client | Install with | What you get |
| --- | --- | --- |
| Claude Code | `--client claude` | Skills in `.claude/skills/`, which Claude Code discovers and selects by their `description`. Add `Follow .claude/RULES.md` to your `CLAUDE.md`. |
| GitHub Copilot (VS Code) | `--client copilot` | Skills in `.agents/skills/`, plus **profiles** as Copilot custom agents (`.github/agents/*.agent.md`) and **prompt files** (`.github/prompts/*.prompt.md`). |
| Codex and others | `--client codex` | Skills in `.agents/skills/`. Reference `.agents/RULES.md` from `AGENTS.md`, and name a skill by path if your version does not discover it. |

## Profiles are Copilot agents

The files in `.github/agents/` use the VS Code Copilot custom-agent format. Claude Code subagents use a different format and folder (`.claude/agents/`), so these profiles do not appear as Claude Code agents. Claude Code users get the same procedures from the skills; a profile adds only a role description and routing, which the skills' own scope and steps already cover.

## Personal skills in Claude Code

To use the skills in every project, install into your home directory:

```bash
python3 scripts/install.py ~ --client claude --collection homelab
```

This creates `~/.claude/skills/`, `~/.claude/RULES.md` and `~/.claude/project/`. The project pages there are generic templates; per-project facts belong in each project.

## Notes

Automatic discovery varies by client version, workspace and session mode. Profiles inherit the tools available to the client; they do not install runtimes or schedule work. There are no automatic agent handoffs.

Official references: [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude memory](https://code.claude.com/docs/en/memory), [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex skills](https://developers.openai.com/codex/skills), [VS Code agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents), [VS Code prompts](https://code.visualstudio.com/docs/copilot/customization/prompt-files).

Validation covers structure, links and installation layout, not behavior in every client.
