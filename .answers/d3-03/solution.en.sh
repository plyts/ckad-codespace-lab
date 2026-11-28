#!/usr/bin/env bash
# Reference solution: d3-03 — TCP readiness probe on a Deployment
kubectl config use-context ckad-a
kubectl -n d3-03 patch deploy api --type=json -p '[{"op":"add",
  "path":"/spec/template/spec/containers/0/readinessProbe",
  "value":{"tcpSocket":{"port":5678},"initialDelaySeconds":2,"periodSeconds":5}}]'
kubectl -n d3-03 rollout status deploy/api --timeout=120s
# VARIANT: kubectl -n d3-03 edit deploy api (more natural in the exam with vim).
