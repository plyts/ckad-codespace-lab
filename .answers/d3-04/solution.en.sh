#!/usr/bin/env bash
# Reference solution: d3-04 — CrashLoopBackOff
kubectl config use-context ckad-a
# Wait for the first crash (a Pod that just started has no Last State yet)
until kubectl -n d3-04 get pod -l app=worker -o jsonpath='{..restartCount}' | grep -q '[1-9]'; do sleep 2; done
kubectl -n d3-04 get pods                                               # CrashLoopBackOff
kubectl -n d3-04 describe pod -l app=worker | grep -A4 'Last State'     # Exit Code: 127
kubectl -n d3-04 get pod -l app=worker -o jsonpath='{.items[0].status.containerStatuses[0].lastState.terminated.exitCode}' \
  > ~/ckad/d3-04/exit-code.txt
kubectl -n d3-04 logs -l app=worker --previous      # sh: slep: not found
kubectl -n d3-04 patch deploy worker --type=json \
  -p '[{"op":"replace","path":"/spec/template/spec/containers/0/command","value":["sh","-c","echo démarrage; sleep 3600"]}]'
kubectl -n d3-04 rollout status deploy/worker --timeout=120s
