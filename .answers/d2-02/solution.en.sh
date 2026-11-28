#!/usr/bin/env bash
# Reference solution: d2-02 — Scaling
kubectl config use-context ckad-a
kubectl -n d2-02 scale deployment front --replicas=5
kubectl -n d2-02 rollout status deploy/front --timeout=120s
