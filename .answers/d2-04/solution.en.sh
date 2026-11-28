#!/usr/bin/env bash
# Reference solution: d2-04 — Rollback after a failed update
kubectl config use-context ckad-a
kubectl -n d2-04 get pods                        # ErrImagePull / ImagePullBackOff
kubectl -n d2-04 rollout history deploy/front
kubectl -n d2-04 rollout undo deploy/front       # or: --to-revision=1
kubectl -n d2-04 rollout status deploy/front --timeout=120s
# Why the old Pods were still running: maxUnavailable (25%) kept the old ReplicaSet.
