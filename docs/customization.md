# Customize for your project

After installing, fill in the project pages (`.claude/project/` or `.agents/project/`) with your actual source paths, document root, config directory, local environment, checks, hosts and deployment commands. Write "unknown" rather than guessing, and keep credentials and private addresses out of anything others can read.

Merge the shared rules into your existing guidance rather than replacing it. A single line in `AGENTS.md` or `CLAUDE.md` pointing to `RULES.md` is enough. Keep your project's own access, ownership and safety rules; they take precedence.

Adapt Composer procedures to your actual root packages, and verify version targets against official sources when you run them.

Try assessment and review workflows on a disposable branch first. Compare the findings with the code and real command output, and note which client, version and workflow you used and what needed manual correction. The [evaluation cases](../evals/README.md) give a repeatable way to do this.
