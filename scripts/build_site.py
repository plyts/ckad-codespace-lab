#!/usr/bin/env python3
"""Construit le guide HTML (site/) à partir de docs/*.md, des captures réelles (docs/_captures)
et du contenu du dépôt (exercices, scénarios, examens blancs corrigés).

Syntaxe propre au guide, dans les .md :
  {{capture:nom}}          sortie réelle enregistrée par scripts/capture-docs.sh
  :::piege Titre … :::     encadré « Piège vérifié » (aussi : pourquoi, verif, examen)
  {{exercices:3}}          liste des exercices du domaine 3
"""
import html
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("module markdown absent : pip install -r docs/requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
CAPS = DOCS / "_captures"
sys.path.insert(0, str(ROOT / "bin"))

COLORS = {"gris": "#6b7280", "bleu": "#2563eb", "jaune": "#ca8a04", "vert": "#16a34a",
          "orange": "#ea580c", "violet": "#7c3aed"}
DOMAIN_COLOR = {"1": "bleu", "2": "jaune", "3": "vert", "4": "orange", "5": "violet", "0": "gris"}
CALLOUTS = {"piege": "Piège vérifié", "pourquoi": "Pourquoi", "verif": "Vérification à la main",
            "examen": "À l'examen"}

# Ordre de navigation : (fichier, titre court, couleur)
NAV = [
    ("index", "Accueil", "gris"),
    ("mode-emploi", "Mode d'emploi", "gris"),
    ("installation", "0 · Le labo", "gris"),
    ("fondamentaux", "Fondamentaux", "gris"),
    ("d1-design-build", "1 · Design and Build", "bleu"),
    ("d2-deployment", "2 · Deployment", "jaune"),
    ("d3-observability", "3 · Observability", "vert"),
    ("d4-config-security", "4 · Config and Security", "orange"),
    ("d5-networking", "5 · Services and Networking", "violet"),
    ("fil-conducteur", "Fil conducteur", "gris"),
    ("commandes", "Commandes kubectl", "gris"),
    ("journal", "Journal des erreurs", "gris"),
    ("examen", "Conditions d'examen", "gris"),
    ("examens-blancs", "Examens blancs corrigés", "gris"),
    ("exercices", "Tous les exercices", "gris"),
    ("cheatsheet", "Cheatsheet", "gris"),
]


def load_units():
    import importlib.machinery, importlib.util
    loader = importlib.machinery.SourceFileLoader("exmod", str(ROOT / "bin" / "ex"))
    spec = importlib.util.spec_from_loader("exmod", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


EX = load_units()


def front(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
    return {k.strip(): v.strip() for k, v in meta.items()}, m.group(2)


def capture_block(name):
    f = CAPS / f"{name}.txt"
    if not f.exists():
        return f'\n<div class="callout missing"><b>NON CAPTURÉ</b> : <code>{name}</code> — lance <code>scripts/capture-docs.sh</code>.</div>\n'
    mf = CAPS / ("journal.meta" if name.startswith("err-") else "guide.meta")
    meta = mf.read_text().strip() if mf.exists() else "date de capture inconnue"
    body = colorize(html.escape(f.read_text().rstrip()))
    return (f'\n<figure class="term"><pre class="terminal"><code>{body}</code></pre>'
            f'<figcaption>Sortie réelle · {html.escape(meta)}</figcaption></figure>\n')


TERM_RULES = [
    (r"\b(PASS|Running|Ready|Bound|Completed|Complete|yes|deployed|successfully rolled out|Labo conforme\.?)\b", "ok"),
    (r"\b(Pending|WARN|ContainerCreating|Terminating|SKIP|superseded)\b", "warn"),
    (r"\b(FAIL|Error|CrashLoopBackOff|ImagePullBackOff|ErrImagePull|OOMKilled|CreateContainerConfigError|"
     r"FailedScheduling|FailedMount|Forbidden|Invalid|refused|timed out|no|BackOff|Failed)\b", "err"),
]


def colorize(txt):
    out = []
    for line in txt.split("\n"):
        if line.startswith("$ "):
            out.append(f'<span class="prompt">$</span> <span class="cmd">{line[2:]}</span>')
            continue
        for rx, cls in TERM_RULES:
            line = re.sub(rx, lambda m, c=cls: f'<span class="t-{c}">{m.group(0)}</span>', line)
        out.append(line)
    return "\n".join(out)


def exercise_list(domain):
    rows = ["| Exercice | Niveau | Temps | Titre |", "|---|---|---|---|"]
    for u in EX.all_units():
        if u.kind == "exercise" and u.domain == domain:
            rows.append(f"| `{u.id}` | {u.level} | {u.time} min | {u.title} |")
    return "\n".join(rows) + "\n\nLance-les avec `ex start <id>` ; les réponses restent cachées jusqu'à `ex solution <id>`."


def preprocess(md):
    md = re.sub(r"\{\{capture:([a-z0-9-]+)\}\}", lambda m: capture_block(m.group(1)), md)
    md = re.sub(r"\{\{exercices:(\d)\}\}", lambda m: exercise_list(m.group(1)), md)

    def callout(m):
        kind, title, body = m.group(1), (m.group(2) or "").strip(), m.group(3)
        label = CALLOUTS[kind] + (f" — {title}" if title else "")
        return f'\n<div class="callout {kind}" markdown="1">\n<p class="callout-title">{label}</p>\n\n{body}\n</div>\n'
    md = re.sub(r"^:::(piege|pourquoi|verif|examen)[ \t]*(.*?)\n(.*?)\n:::[ \t]*$", callout, md, flags=re.M | re.S)
    return md


def gen_exercices():
    parts = ["---\ntitle: Tous les exercices\ncolor: gris\n---\n# Tous les exercices\n",
             "Chaque exercice se lance avec `ex start <id>` et se vérifie avec `ex check <id>`. "
             "Les consignes ci-dessous sont celles du terminal ; les solutions n'apparaissent pas ici.\n"]
    for d, (name, w, color, _) in EX.DOMAINS.items():
        parts.append(f'\n## <span class="dot {color}"></span> Domaine {d} — {name} ({w} %)\n')
        for u in EX.all_units():
            if u.kind == "exercise" and u.domain == d:
                parts.append(f"\n### `{u.id}` · {u.title}\n\n*{u.level} · {u.time} min · contexte `{u.ctx}` · "
                             f"namespace `{u.ns}` · [doc]({u.doc})*\n\n{u.body}\n")
    return "\n".join(parts)


def gen_mocks():
    parts = ["---\ntitle: Examens blancs corrigés\ncolor: gris\n---\n# Examens blancs corrigés\n",
             ":::examen\nFais d'abord l'examen dans le labo (`mock start N`, puis `mock grade N` à la sonnerie). "
             "N'ouvre les corrections qu'ensuite : elles sont repliées.\n:::\n"]
    for d in sorted((ROOT / "mock-exams").glob("mock-*")):
        n = d.name.split("-")[1]
        meta, intro = EX.mock_meta(n)
        tasks = EX.mock_tasks(n)
        parts.append(f"\n## Examen blanc {n} — {meta.get('title')} ({meta.get('duration')} min, {len(tasks)} tâches)\n\n{intro}\n")
        parts.append("| # | Poids | Domaine | Contexte | Tâche |\n|---|---|---|---|---|")
        for i, t in enumerate(tasks, 1):
            parts.append(f"| {i} | {t.weight} % | {t.domain} | `{t.ctx}` | {t.title} |")
        for i, t in enumerate(tasks, 1):
            sol = (t.answer_dir / "solution.sh").read_text().split("\n", 2)[-1]
            parts.append(f"\n### Tâche {i} — {t.title} ({t.weight} %)\n\n*contexte `{t.ctx}` · namespace `{t.ns}` · "
                         f"{t.time} min conseillées · [doc]({t.doc})*\n\n{t.body}\n\n"
                         f'<details><summary>Correction commentée</summary>\n\n```bash\n{sol.strip()}\n```\n\n</details>\n')
    return "\n".join(parts)


def gen_scenarios():
    parts = []
    for u in EX.all_units():
        if u.kind == "scenario":
            parts.append(f"\n### `{u.id}` · {u.title}\n\n*{u.time} min · `ex scenario {u.id}`*\n\n{u.body}\n")
    return "\n".join(parts)


TEMPLATE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Labo CKAD</title>
<link rel="stylesheet" href="assets/style.css">
</head><body style="--accent:{accent}">
<div id="progress"></div>
<header class="top"><button id="menu" aria-label="Menu">☰</button><a class="brand" href="index.html">Labo CKAD</a>
<span class="tag">Kubernetes {k8s} · vérifié par l'exécution</span><button id="theme" aria-label="Changer de thème">Thème</button></header>
<nav id="nav">{nav}</nav>
<main><article>{content}</article>
<footer>Guide généré par <code>bin/site build</code> depuis le dépôt. Toutes les sorties de terminal sont des captures réelles
(<code>scripts/capture-docs.sh</code>). Aucune IA dans le labo.</footer></main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/yaml.min.js"></script>
<script src="assets/app.js"></script>
</body></html>
"""


def build():
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    shutil.copy(DOCS / "assets" / "style.css", SITE / "assets")
    shutil.copy(DOCS / "assets" / "app.js", SITE / "assets")
    k8s = re.search(r"K8S_VERSION=(\S+)", (ROOT / "versions.env").read_text()).group(1)
    generated = {"exercices": gen_exercices(), "examens-blancs": gen_mocks()}
    built = 0
    for name, short, color in NAV:
        src = ROOT / "MODE-EMPLOI.md" if name == "mode-emploi" else DOCS / f"{name}.md"
        text = generated.get(name) or (src.read_text(encoding="utf-8") if src.exists() else None)
        if text is None:
            print(f"  (absent) {name}.md")
            continue
        meta, body = front(text)
        if name == "mode-emploi":
            meta = {"title": "Mode d'emploi", "color": "gris"}
        body = body.replace("{{scenarios}}", gen_scenarios())
        md = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "attr_list", "md_in_html", "sane_lists"],
                               extension_configs={"toc": {"permalink": "#", "toc_depth": "2-3"}})
        content = md.convert(preprocess(body))
        toc = md.toc if "<li>" in md.toc else ""
        nav = []
        for n2, s2, c2 in NAV:
            cur = ' class="current"' if n2 == name else ""
            nav.append(f'<a href="{n2}.html"{cur} style="--c:{COLORS[c2]}"><span class="dot" style="background:{COLORS[c2]}"></span>{s2}</a>')
            if n2 == name and toc:
                nav.append(f'<div class="toc">{toc}</div>')
        page = TEMPLATE.format(title=html.escape(meta.get("title", short)), accent=COLORS[meta.get("color", color)],
                               nav="\n".join(nav), content=content, k8s=k8s)
        (SITE / f"{name}.html").write_text(page, encoding="utf-8")
        built += 1
    print(f"site/ : {built} pages")


if __name__ == "__main__":
    build()
