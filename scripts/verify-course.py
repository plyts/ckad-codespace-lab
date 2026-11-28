#!/usr/bin/env python3
"""Vérifie le cours (course/course.py) par l'exécution, sur le contexte ckad-a.

- Chaque bloc de commandes marqué exécutable est lancé dans l'ordre, avec bash -e (un échec = FAIL).
- Chaque YAML est validé par le serveur d'API : kubectl apply --dry-run=server -n cours.
- Une notion qui demande une capacité absente (netpol, metrics) est SKIP ; une notion illustrative
  (run=None) est signalée comme telle et n'est jamais présentée comme vérifiée.
Résultat : .progress/course-verify.json ; code retour 1 si un FAIL.
Usage : scripts/verify-course.py [id-de-notion …]
"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "course"))
import course  # noqa: E402

TTY = sys.stdout.isatty()
CAPD = ROOT / "docs" / "_captures" / "course"

MASKS = [  # mêmes masques que scripts/capture-docs.sh : âges, horodatages, hachages
    (r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.]+Z", "<horodatage>"),
    (r"\(([0-9]+[smhd])+ ago\)", "(il y a <durée>)"),
    (r"(?<=\s)[0-9]+[smhd]([0-9]+[smh])?(?=\s|$)", "<âge>"),
    (r"\(x[0-9]+ over [0-9a-z]+\)", "(xN sur <durée>)"),
]


def mask(txt):
    import re
    for rx, rep in MASKS:
        txt = re.sub(rx, rep, txt, flags=re.M)
    return txt


def col(c, t):
    return f"\033[{c}m{t}\033[0m" if TTY else t


def caps():
    f = ROOT / ".progress" / "caps"
    out = {}
    if f.exists():
        for line in f.read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                out[k] = v == "1"
    return out


def sh(cmd, env, cwd, timeout=420, stdin=None):
    return subprocess.run(["bash", "-e", "-c", cmd], env=env, cwd=cwd, text=True, input=stdin,
                          capture_output=True, timeout=timeout)


def main():
    only = set(sys.argv[1:])
    work = Path(tempfile.mkdtemp(prefix="cours-"))
    kc = work / "kubeconfig"
    kc.write_text(subprocess.run(["kubectl", "config", "view", "--flatten"], text=True, capture_output=True).stdout)
    env = dict(os.environ, KUBECONFIG=str(kc), ROOT=str(ROOT), do="--dry-run=client -o yaml",
               now="--force --grace-period 0", PATH=f"{ROOT}/bin:{os.environ['PATH']}")
    sh("kubectl config use-context ckad-a >/dev/null", env, work)
    if not only:
        print(col("90", "Remise à zéro : namespaces cours et cours-b, objets de cluster du cours…"))
        sh("""kubectl delete ns cours cours-b --ignore-not-found --wait=true --timeout=180s
              kubectl delete pv cours-pv --ignore-not-found
              kubectl delete crd certificats.cours.lab --ignore-not-found
              kubectl delete clusterrole,clusterrolebinding cours-node-viewer --ignore-not-found
              kubectl label node ckad-a-worker disk- 2>/dev/null || true
              kubectl taint node ckad-a-worker2 dedie- 2>/dev/null || true
              kubectl create ns cours
              until kubectl -n cours get sa default >/dev/null 2>&1; do sleep 1; done""", env, work, timeout=300)
    have = caps()
    results, nfail = [], 0
    for ch in course.CHAPTERS:
        for c in ch["concepts"]:
            if only and c["id"] not in only:
                continue
            t0 = time.time()
            verdict, note = "PASS", ""
            req = c.get("requires")
            if req and not have.get(f"{req}@ckad-a", False):
                verdict, note = "SKIP", f"capacité absente : {req}"
            else:
                if c["run"] is not None and c["cmd"]:
                    script = textwrap.dedent(c["cmd"] if c["run"] is True else c["run"]).strip()
                    try:
                        r = sh(script, env, work)
                        if r.returncode != 0:
                            verdict, note = "FAIL", (r.stdout + r.stderr)[-1500:]
                        else:
                            CAPD.mkdir(parents=True, exist_ok=True)
                            (CAPD / f"{c['id']}.txt").write_text(mask((r.stdout + r.stderr).strip()) + "\n")
                    except subprocess.TimeoutExpired:
                        verdict, note = "FAIL", "délai dépassé"
                elif c["run"] is None:
                    verdict, note = "ILLUSTRATIF", "commandes non exécutées (montrées pour la méthode)"
                if verdict != "FAIL" and c.get("yaml"):
                    r = subprocess.run(["kubectl", "apply", "--dry-run=server", "-n", "cours", "-f", "-"],
                                       input=textwrap.dedent(c["yaml"]), env=env, text=True, capture_output=True)
                    if r.returncode != 0:
                        verdict, note = "FAIL", "YAML refusé par l'API : " + (r.stdout + r.stderr)[-800:]
                    else:
                        note = (note + " ; " if note else "") + "YAML validé (dry-run=server)"
            dur = int(time.time() - t0)
            colour = {"PASS": "32", "FAIL": "31", "SKIP": "90", "ILLUSTRATIF": "90"}[verdict]
            print(f"{col(colour, f'{verdict:<11}')} {ch['id']:<6} {c['id']:<16} {dur:>4}s  {note.splitlines()[0] if note else ''}")
            if verdict == "FAIL":
                nfail += 1
                print(col("90", "      " + "\n      ".join(note.splitlines()[-15:])))
            results.append({"chapter": ch["id"], "id": c["id"], "verdict": verdict, "note": note, "seconds": dur})
    (ROOT / ".progress").mkdir(exist_ok=True)
    (ROOT / ".progress" / "course-verify.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    if not only:  # trace publiée avec le guide : où et quand le cours a été exécuté
        CAPD.mkdir(parents=True, exist_ok=True)
        kv = subprocess.run(["kubectl", "version", "-o", "json"], env=env, text=True, capture_output=True).stdout
        try:
            k8s = json.loads(kv)["serverVersion"]["gitVersion"]
        except Exception:
            k8s = "?"
        (CAPD / "verify.json").write_text(json.dumps({
            "date": time.strftime("%Y-%m-%d"), "host": os.uname().nodename, "kubernetes": k8s,
            "results": {r["id"]: r["verdict"] for r in results}}, indent=1, ensure_ascii=False))
    n = len(results)
    print(f"\n{n - nfail}/{n} notions sans échec "
          f"({sum(r['verdict'] == 'PASS' for r in results)} exécutées, "
          f"{sum(r['verdict'] == 'SKIP' for r in results)} SKIP, "
          f"{sum(r['verdict'] == 'ILLUSTRATIF' for r in results)} illustratives)")
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
