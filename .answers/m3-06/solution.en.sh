#!/usr/bin/env bash
# Reference solution: m3-06 — Recreate strategy
kubectl config use-context ckad-a

kubectl -n m3-06 patch deploy legacy --type=json -p '[{"op":"replace","path":"/spec/strategy","value":{"type":"Recreate"}}]'
kubectl -n m3-06 set image deploy/legacy nginx=nginx:1.28-alpine
kubectl -n m3-06 rollout status deploy/legacy --timeout=120s
