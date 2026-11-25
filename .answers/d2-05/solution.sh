#!/usr/bin/env bash
# Solution de référence : d2-05 — Régler la stratégie de déploiement
kubectl config use-context ckad-a
kubectl -n d2-05 patch deploy api --type=merge -p '{
  "spec": {
    "minReadySeconds": 5,
    "revisionHistoryLimit": 4,
    "strategy": {"type": "RollingUpdate", "rollingUpdate": {"maxSurge": 1, "maxUnavailable": 0}}
  }}'
kubectl -n d2-05 get deploy api -o yaml | grep -E -A4 'strategy|minReady|revisionHistory'
# VARIANTE : kubectl -n d2-05 edit deploy api, puis modifier les mêmes champs dans vim.
