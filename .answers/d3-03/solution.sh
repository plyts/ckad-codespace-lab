#!/usr/bin/env bash
# Solution de référence : d3-03 — Readiness probe TCP sur un Deployment
kubectl config use-context ckad-a
kubectl -n d3-03 patch deploy api --type=json -p '[{"op":"add",
  "path":"/spec/template/spec/containers/0/readinessProbe",
  "value":{"tcpSocket":{"port":5678},"initialDelaySeconds":2,"periodSeconds":5}}]'
kubectl -n d3-03 rollout status deploy/api --timeout=120s
# VARIANTE : kubectl -n d3-03 edit deploy api (plus naturel à l'examen avec vim).
