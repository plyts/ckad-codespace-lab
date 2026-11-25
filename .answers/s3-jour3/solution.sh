#!/usr/bin/env bash
# Solution de référence : s3-jour3 — Boutique, journée 3 : incident et rollback
kubectl config use-context ckad-a
kubectl -n boutique-j3 get pods -l app=api            # les Pods v2 : Error / CrashLoopBackOff
# Un Pod de la révision v2 (son argument est -text=api v2). Ne pas le choisir par son statut :
# un conteneur qui plante repasse brièvement en Running à chaque redémarrage.
pod=""
until [ -n "$pod" ]; do
  pod=$(kubectl -n boutique-j3 get pods -l app=api \
    -o jsonpath='{range .items[?(@.spec.containers[0].args[0]=="-text=api v2")]}{.metadata.name}{"\n"}{end}' | head -1)
  sleep 1
done
until kubectl -n boutique-j3 get pod "$pod" --no-headers | grep -qE 'CrashLoopBackOff|Error'; do sleep 1; done
kubectl -n boutique-j3 get pod "$pod" --no-headers | awk '{print $3}' > ~/ckad/s3-jour3/incident.txt
# Le conteneur est mort : ses logs sont ceux de l'instance courante ou, sinon, --previous
until { kubectl -n boutique-j3 logs "$pod" 2>/dev/null; kubectl -n boutique-j3 logs "$pod" --previous 2>/dev/null; } | grep -q 'flag provided'; do sleep 1; done
{ kubectl -n boutique-j3 logs "$pod" 2>/dev/null; kubectl -n boutique-j3 logs "$pod" --previous 2>/dev/null; } \
  | grep -m1 'flag provided' >> ~/ckad/s3-jour3/incident.txt     # flag provided but not defined: -timeout
cat ~/ckad/s3-jour3/incident.txt
kubectl -n boutique-j3 rollout history deploy/api
kubectl -n boutique-j3 rollout undo deploy/api
kubectl -n boutique-j3 rollout status deploy/api --timeout=180s
