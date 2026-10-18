# Tool compatibility

The portable baseline is explicit file reading: ask your assistant to read AGENTS.md, the selected SKILL.md and relevant project references.

| Client | Entry point |
| --- | --- |
| Claude Code | CLAUDE.md imports AGENTS.md; request the skill by path, or install it for discovery (below) |
| Codex | Use repository guidance and explicitly provide the skill path; verify discovery in your installed client |
| GitHub Copilot / VS Code | Profiles and prompt files are supplied; verify availability and supported frontmatter in your installed version; fall back to explicit paths |

## Claude Code skill discovery

Claude Code discovers project skills in `.claude/skills/<name>/SKILL.md` (or personal skills in `~/.claude/skills/`) and selects them by their `description`. This toolkit keeps skills in the client-neutral `.agents/skills/`, so either name the skill path in your request or copy the skills you adopted into the discovered location in your project:

```bash
mkdir -p .claude/skills
cp -R .agents/skills/drupal-upgrade-assessment .claude/skills/
```

A directory symlink (`ln -s ../.agents/skills .claude/skills`) avoids two copies on Linux and macOS, but Git on Windows checks symlinks out as plain files unless symlink support is enabled. Skill-relative links such as `../../../AGENTS.md` assume the skill sits two folders below the project root, which both locations satisfy.

## Notes

Automatic discovery varies by client version, workspace and session mode. Profiles inherit available tools; they do not install runtimes or schedule work. There are no automatic agent handoffs.

Official references: [Claude memory](https://code.claude.com/docs/en/memory), [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex skills](https://developers.openai.com/codex/skills), [VS Code agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents), [VS Code prompts](https://code.visualstudio.com/docs/copilot/customization/prompt-files).

Public edition validation covers structure and links, not execution across all these clients.
