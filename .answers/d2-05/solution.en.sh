#!/usr/bin/env bash
# Reference solution: d2-05 — Tuning the deployment strategy
kubectl config use-context ckad-a
kubectl -n d2-05 patch deploy api --type=merge -p '{
  "spec": {
    "minReadySeconds": 5,
    "revisionHistoryLimit": 4,
    "strategy": {"type": "RollingUpdate", "rollingUpdate": {"maxSurge": 1, "maxUnavailable": 0}}
  }}'
kubectl -n d2-05 get deploy api -o yaml | grep -E -A4 'strategy|minReady|revisionHistory'
# VARIANT: kubectl -n d2-05 edit deploy api, then change the same fields in vim.
