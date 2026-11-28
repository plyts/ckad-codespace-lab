#!/usr/bin/env bash
# Reference solution: d2-01 — First Deployment
kubectl config use-context ckad-a
kubectl -n d2-01 create deployment front --image=nginx:1.27-alpine --replicas=3
kubectl -n d2-01 rollout status deploy/front --timeout=120s
# Deployment → ReplicaSet → Pods:
kubectl -n d2-01 get deploy,rs,pods -l app=front
