#!/usr/bin/env bash
# Solution de référence : d2-02 — Mise à l'échelle
kubectl config use-context ckad-a
kubectl -n d2-02 scale deployment front --replicas=5
kubectl -n d2-02 rollout status deploy/front --timeout=120s
