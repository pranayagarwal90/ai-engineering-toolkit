"""Run evaluation cases with the Claude Code CLI: baseline vs skill, then a blind rubric grade.

    python3 evals/run_claude.py --claude /path/to/claude --model claude-opus-5-5 [--case ID ...]

For each case:
- baseline: a throwaway empty directory, no tools, only the case's Task and Evidence
- skill:    a throwaway directory with the case's skill installed by scripts/install.py
            (--client claude), the Read tool only, and an instruction to read RULES.md and the skill
- grade:    a separate run sees the rubric and both answers as "A" and "B" in random order,
            and returns per-item scores as JSON

MCP servers are disabled (--strict-mcp-config) and sessions are not persisted. Run it from a
directory tree without CLAUDE.md or AGENTS.md files so no project guidance leaks in. Answers, grades
and a summary are written to evals/results/runs/<date>-<model>/.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "cases"
FRAME = ("You are an AI coding assistant. A user sent the message below with the evidence shown. Answer as you "
         "would in a real session. You have no access to the user's systems and cannot run commands here; where "
         "you would act, say what you would do and which commands you would run. Reply with only your answer "
         "to the user.\n\n")


def section(text, name):
    match = re.search(rf"^## {name}\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match.group(1).strip() if match else ""


def load_case(path):
    text = path.read_text(encoding="utf-8")
    skill = re.search(r"^skill: \.agents/skills/([a-z0-9-]+)/SKILL\.md$", text, re.M).group(1)
    task = section(text, "Task").lstrip("> ").replace("\n> ", "\n")
    return {"id": path.stem, "skill": skill, "pass": int(re.search(r"^pass: (\d+)$", text, re.M).group(1)),
            "prompt": f"USER MESSAGE:\n{task}\n\nEVIDENCE:\n{section(text, 'Evidence')}",
            "rubric": section(text, "Rubric"),
            "must": len(re.findall(r"^\d+\. ", section(text, "Rubric").split("**Must not:**")[0], re.M))}


def claude(binary, model, prompt, cwd, tools):
    cmd = [binary, "-p", "--no-session-persistence", "--strict-mcp-config", "--model", model, "--tools", tools]
    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd, timeout=600)
    if result.returncode:
        raise RuntimeError(f"claude failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def run_case(case, binary, model):
    with tempfile.TemporaryDirectory(prefix="eval-baseline-") as empty:
        baseline = claude(binary, model, FRAME + case["prompt"], empty, "")
    with tempfile.TemporaryDirectory(prefix="eval-skill-") as project:
        subprocess.run([sys.executable, str(ROOT / "scripts/install.py"), project, "--client", "claude",
                        "--skill", case["skill"]], check=True, capture_output=True)
        lead = (f"First read .claude/RULES.md and .claude/skills/{case['skill']}/SKILL.md and follow them. "
                "Read no other files.\n\n")
        skill = claude(binary, model, FRAME + lead + case["prompt"], project, "Read")
    return baseline, skill


def grade(case, answers, binary, model, rng):
    order = ["baseline", "skill"]
    rng.shuffle(order)
    labelled = {"A": answers[order[0]], "B": answers[order[1]]}
    prompt = (
        "You are grading two assistant answers to the same task against a rubric. Judge only what each answer "
        "says or proposes. A Must item is met (1) only if the answer clearly does it; otherwise 0. List every "
        "Must-not item an answer violates, quoting the words that violate it.\n\n"
        f"TASK AND EVIDENCE:\n{case['prompt']}\n\nRUBRIC:\n{case['rubric']}\n\n"
        f"ANSWER A:\n{labelled['A']}\n\nANSWER B:\n{labelled['B']}\n\n"
        f"Reply with only JSON: {{\"A\": {{\"must\": [{case['must']} zeros or ones], \"violations\": [\"...\"], "
        "\"notes\": \"one sentence\"}, \"B\": {...same...}}")
    with tempfile.TemporaryDirectory(prefix="eval-grade-") as empty:
        raw = claude(binary, model, prompt, empty, "")
    data = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
    return {order[0]: data["A"], order[1]: data["B"]}, order


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--claude", default="claude", help="Path to the Claude Code CLI.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--case", nargs="*", help="Case ids (default: all).")
    parser.add_argument("--seed", type=int, default=0, help="Seed for the blind A/B order.")
    args = parser.parse_args(argv)

    paths = [CASES / f"{c}.md" for c in args.case] if args.case else sorted(CASES.glob("*.md"))
    out = ROOT / "evals/results/runs" / f"{dt.date.today().isoformat()}-{args.model}"
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    summary = []
    for path in paths:
        case = load_case(path)
        print(f"{case['id']}: running", flush=True)
        baseline, skill = run_case(case, args.claude, args.model)
        answers = {"baseline": baseline, "skill": skill}
        for name, text in answers.items():
            (out / f"{case['id']}.{name}.md").write_text(text + "\n", encoding="utf-8")
        scores, order = grade(case, answers, args.claude, args.model, rng)
        (out / f"{case['id']}.grade.json").write_text(
            json.dumps({"shown_as": {"A": order[0], "B": order[1]}, **scores}, indent=2) + "\n", encoding="utf-8")
        row = {"case": case["id"], "pass_mark": case["pass"], "must_items": case["must"]}
        for name in ("baseline", "skill"):
            score, violations = sum(scores[name]["must"]), scores[name]["violations"]
            row[name] = {"score": score, "violations": violations, "pass": score >= case["pass"] and not violations}
        summary.append(row)
        print(f"  baseline {row['baseline']['score']}/{case['must']}  skill {row['skill']['score']}/{case['must']}",
              flush=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Results in {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
