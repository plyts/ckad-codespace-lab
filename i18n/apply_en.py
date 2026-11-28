#!/usr/bin/env python3
"""Writes the English files of every unit from i18n/en_*.py.

  task.en.md     front matter (title) + instructions
  hints.en.md    ## Hint N
  check.en.txt   one line per check, in runtime order: title|||why
  exam.en.md     mock exam header
  .answers/<id>/solution.en.sh   same commands, comments in English

Refuses (exit 1) any unit without a translation, any check count that differs from check.sh, and any
French comment of a solution that i18n/en_solutions.py does not know. Run it again after every change
to a task, a check or a solution:  python3 i18n/apply_en.py   (--check: compare only, write nothing)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "i18n"))
from en_units import UNITS          # noqa: E402
import en_mocks                      # noqa: E402
from en_solutions import COMMENTS    # noqa: E402

CHECK_ONLY = "--check" in sys.argv
errors, written = [], []
FRENCH = re.compile(r"[éèàùâêîôûçœÉÈÀ]|\b(le|la|les|des|du|une|et|pour|sans|avec|puis|est|sont)\b")
CK = re.compile(r"^\s*ck_(eq|match|true|http|http_blocked|tcp|tcp_blocked)\s")


def front(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def count_checks(check_sh):
    """Number of checks the file runs (loops expanded: `for x in a b c` and `$(echo a,b | tr , ' ')`)."""
    n, mult = 0, 1
    for line in check_sh.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*for \w+ in (.*); do\s*$", line)
        if m:
            items = m.group(1)
            e = re.match(r"\$\(echo (\S+) \| tr , ' '\)", items)
            mult = len(e.group(1).split(",")) if e else len(items.split())
            continue
        if re.match(r"^\s*done\s*$", line):
            mult = 1
            continue
        if CK.match(line):
            n += mult
    return n


def write(path, text):
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return
    if CHECK_ONLY:
        errors.append(f"{path.relative_to(ROOT)}: out of date (run python3 i18n/apply_en.py)")
        return
    path.write_text(text, encoding="utf-8")
    written.append(path)


def one_line(s):
    return " ".join(s.split())


def apply_unit(udir, uid, title, body, hints, checks):
    n = count_checks(udir / "check.sh")
    if n != len(checks):
        errors.append(f"{uid}: check.sh runs {n} checks, the translation has {len(checks)}")
        return
    meta, _ = front((udir / "task.md").read_text(encoding="utf-8"))
    write(udir / "task.en.md", f"---\nid: {uid}\ntitle: {title}\n---\n{body.strip()}\n")
    if len(hints) != 3:
        errors.append(f"{uid}: {len(hints)} hints instead of 3")
    write(udir / "hints.en.md", "".join(f"## Hint {i}\n\n{h.strip()}\n\n" for i, h in enumerate(hints, 1)))
    lines = []
    for t, w in checks:
        if "|||" in t or "|||" in w:
            errors.append(f"{uid}: '|||' inside a check text")
        lines.append(f"{one_line(t)}|||{one_line(w)}")
    write(udir / "check.en.txt", "\n".join(lines) + "\n")
    apply_solution(uid, title)


def translate_comment(uid, text):
    if text in COMMENTS:
        return COMMENTS[text]
    if FRENCH.search(text):
        errors.append(f"{uid}: French comment without translation: {text!r}")
    return text


def apply_solution(uid, title_en):
    src = ROOT / ".answers" / uid / "solution.sh"
    if not src.exists():
        errors.append(f"{uid}: .answers/{uid}/solution.sh missing")
        return
    out = []
    for line in src.read_text(encoding="utf-8").splitlines():
        if line.startswith("#!"):
            out.append(line)
        elif line.startswith("# Solution de référence"):
            out.append(f"# Reference solution: {uid} — {title_en}")
        elif re.match(r"^\s*# ", line):
            ind, text = re.match(r"^(\s*# )(.*)$", line).groups()
            out.append(ind + translate_comment(uid, text))
        else:
            m = re.match(r"^(.*\S\s+# )(.*)$", line)
            if m and m.group(2) in COMMENTS:
                out.append(m.group(1) + COMMENTS[m.group(2)])
            elif m and FRENCH.search(m.group(2)) and "'" not in m.group(2) and '"' not in m.group(2):
                errors.append(f"{uid}: French comment without translation: {m.group(2)!r}")
                out.append(line)
            else:
                out.append(line)
    dst = ROOT / ".answers" / uid / "solution.en.sh"
    write(dst, "\n".join(out) + "\n")
    if not CHECK_ONLY and dst.exists():
        dst.chmod(0o755)


def main():
    seen = set()
    for task in sorted(ROOT.glob("exercises/*/*/task.md")) + sorted(ROOT.glob("scenarios/*/task.md")):
        uid = front(task.read_text(encoding="utf-8"))[0]["id"]
        seen.add(uid)
        if uid not in UNITS:
            errors.append(f"{uid}: no English translation in i18n/en_units.py")
            continue
        u = UNITS[uid]
        apply_unit(task.parent, uid, u["title"], u["body"], u["hints"], u["checks"])
    for uid in sorted(set(UNITS) - seen):
        errors.append(f"{uid}: translated but no such unit")

    for n, plan in en_mocks.PLAN.items():
        mdir = ROOT / "mock-exams" / f"mock-{n}"
        meta, _ = front((mdir / "exam.md").read_text(encoding="utf-8"))
        title, intro = en_mocks.EXAMS[n]
        write(mdir / "exam.en.md", f"---\nduration: {meta['duration']}\ntitle: {title}\n---\n{intro}\n\n{en_mocks.RULES}\n")
        tasks = sorted((mdir / "tasks").glob("*/task.md"))
        if len(tasks) != len(plan):
            errors.append(f"mock-{n}: {len(tasks)} tasks, {len(plan)} translations")
            continue
        for task, (ttitle, fn) in zip(tasks, plan):
            tmeta, _ = front(task.read_text(encoding="utf-8"))
            uid = tmeta["id"]
            kw = fn(uid, tmeta["context"])
            apply_unit(task.parent, uid, ttitle, kw["body"], kw["hints"], kw["checks"])

    for e in errors:
        print("ERROR", e)
    verb = "to update" if CHECK_ONLY else "written"
    print(f"{len(written)} file(s) {verb}, {len(errors)} error(s)")
    sys.exit(1 if errors else 0)


main()
