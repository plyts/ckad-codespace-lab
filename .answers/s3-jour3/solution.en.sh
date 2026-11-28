#!/usr/bin/env bash
# Reference solution: s3-jour3 — Shop, day 3: incident and rollback
kubectl config use-context ckad-a
kubectl -n boutique-j3 get pods -l app=api            # the v2 Pods: Error / CrashLoopBackOff
# A Pod of revision v2 (its argument is -text=api v2). Do not pick it by its status:
# a crashing container is briefly Running again at each restart.
pod=""
until [ -n "$pod" ]; do
  pod=$(kubectl -n boutique-j3 get pods -l app=api \
    -o jsonpath='{range .items[?(@.spec.containers[0].args[0]=="-text=api v2")]}{.metadata.name}{"\n"}{end}' | head -1)
  sleep 1
done
# Read the status once and record that value: read again later, it may already be Running.
st=""
until [[ "$st" == CrashLoopBackOff || "$st" == Error ]]; do
  st=$(kubectl -n boutique-j3 get pod "$pod" --no-headers | awk '{print $3}'); sleep 1
done
echo "$st" > ~/ckad/s3-jour3/incident.txt
# The container died: its logs are those of the current instance or, otherwise, --previous
until { kubectl -n boutique-j3 logs "$pod" 2>/dev/null; kubectl -n boutique-j3 logs "$pod" --previous 2>/dev/null; } | grep -q 'flag provided'; do sleep 1; done
{ kubectl -n boutique-j3 logs "$pod" 2>/dev/null; kubectl -n boutique-j3 logs "$pod" --previous 2>/dev/null; } \
  | grep -m1 'flag provided' >> ~/ckad/s3-jour3/incident.txt     # flag provided but not defined: -timeout
cat ~/ckad/s3-jour3/incident.txt
kubectl -n boutique-j3 rollout history deploy/api
kubectl -n boutique-j3 rollout undo deploy/api
kubectl -n boutique-j3 rollout status deploy/api --timeout=180s
