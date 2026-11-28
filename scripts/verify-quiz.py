#!/usr/bin/env python3
"""Vérifie le QCU (quiz/quiz.py) : structure, puis exécution réelle des commandes de réponse.

1. Structure : identifiants uniques, une seule bonne réponse valide, choix distincts, français et anglais présents.
2. Exécution : dans le namespace « quiz » (contexte ckad-a) préparé avec un Deployment web, un Service web,
   un Pod tool, un Pod multi-conteneurs et un Secret db, chaque script « verify » doit réussir (bash -e).
Résultat : docs/_captures/quiz-verify.json (publié avec le guide) ; code retour 1 si un échec.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "quiz"))
import quiz  # noqa: E402

SETUP = r"""
kubectl delete ns quiz --ignore-not-found --wait=true --timeout=180s
kubectl create ns quiz
until kubectl -n quiz get sa default >/dev/null 2>&1; do sleep 1; done
kubectl -n quiz create deployment web --image=nginx:1.27-alpine --replicas=2 --port=80
kubectl -n quiz expose deploy web --port=80
kubectl -n quiz run tool --image=busybox:1.37 --labels=app=shop,tier=front -- sleep 3600
kubectl -n quiz run dbpod --image=busybox:1.37 --labels=app=shop,tier=db -- sleep 3600
kubectl -n quiz create secret generic db --from-literal='password=S3cr3t!'
kubectl apply -n quiz -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: multi}
spec:
  containers:
  - {name: main, image: "busybox:1.37", command: ["sh", "-c", "sleep 3600"]}
  - {name: side, image: "busybox:1.37", command: ["sh", "-c", "echo side prêt; sleep 3600"]}
EOF
kubectl -n quiz rollout status deploy/web --timeout=180s
kubectl -n quiz wait --for=condition=Ready pod/tool pod/multi --timeout=120s
"""


def check_structure():
    errs, ids = [], set()
    for q in quiz.QUESTIONS:
        qid = q["id"]
        if qid in ids:
            errs.append(f"{qid}: identifiant en double")
        ids.add(qid)
        if q["domain"] not in quiz.DOMAINS:
            errs.append(f"{qid}: domaine inconnu")
        for f in ("q", "why"):
            if not (q[f].get("fr") and q[f].get("en")):
                errs.append(f"{qid}: {f} sans fr/en")
        if not (0 <= q["answer"] < len(q["choices"])):
            errs.append(f"{qid}: index de réponse invalide")
        if len(q["choices"]) < 3:
            errs.append(f"{qid}: moins de 3 choix")
        for lang in ("fr", "en"):
            labels = [c[lang] if isinstance(c, dict) else c for c in q["choices"]]
            if len(set(labels)) != len(labels):
                errs.append(f"{qid}: choix en double ({lang})")
        if not q.get("cmd"):
            errs.append(f"{qid}: pas de commande de réponse")
    return errs


def main():
    errs = check_structure()
    print(f"Structure : {len(quiz.QUESTIONS)} questions, " + (f"{len(errs)} erreur(s)" if errs else "conforme"))
    for e in errs:
        print("  FAIL", e)
    work = Path(tempfile.mkdtemp(prefix="quiz-"))
    kc = work / "kubeconfig"
    kc.write_text(subprocess.run(["kubectl", "config", "view", "--flatten"], text=True, capture_output=True).stdout)
    env = dict(os.environ, KUBECONFIG=str(kc), ROOT=str(ROOT))
    subprocess.run(["kubectl", "config", "use-context", "ckad-a"], env=env, capture_output=True)
    r = subprocess.run(["bash", "-e", "-c", SETUP], env=env, cwd=work, text=True, capture_output=True, timeout=600)
    if r.returncode != 0:
        print("Préparation du namespace quiz en échec :\n" + (r.stdout + r.stderr)[-1500:])
        sys.exit(1)
    results, nfail = {}, len(errs)
    for q in quiz.QUESTIONS:
        if not q.get("verify"):
            results[q["id"]] = "CONCEPT"
            continue
        t0 = time.time()
        try:
            r = subprocess.run(["bash", "-e", "-c", q["verify"]], env=env, cwd=work, text=True,
                               capture_output=True, timeout=180)
            ok = r.returncode == 0
            out = (r.stdout + r.stderr)[-800:]
        except subprocess.TimeoutExpired:
            ok, out = False, "délai dépassé"
        results[q["id"]] = "PASS" if ok else "FAIL"
        print(f"{'PASS' if ok else 'FAIL'}  {q['id']:<20} {int(time.time() - t0):>3}s")
        if not ok:
            nfail += 1
            print("      " + "\n      ".join(out.splitlines()[-8:]))
    n_ok = sum(v == "PASS" for v in results.values())
    n_c = sum(v == "CONCEPT" for v in results.values())
    print(f"\n{n_ok} commandes de réponse exécutées avec succès, {n_c} questions conceptuelles, {nfail} échec(s)")
    out = ROOT / "docs" / "_captures" / "quiz-verify.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"date": time.strftime("%Y-%m-%d"), "host": os.uname().nodename, "results": results},
                              indent=1, ensure_ascii=False))
    subprocess.run(["kubectl", "delete", "ns", "quiz", "--wait=false"], env=env, capture_output=True)
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
