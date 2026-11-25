#!/usr/bin/env bash
# Solution de référence : d2-04 — Rollback après une mise à jour ratée
kubectl config use-context ckad-a
kubectl -n d2-04 get pods                        # ErrImagePull / ImagePullBackOff
kubectl -n d2-04 rollout history deploy/front
kubectl -n d2-04 rollout undo deploy/front       # ou : --to-revision=1
kubectl -n d2-04 rollout status deploy/front --timeout=120s
# Pourquoi les anciens Pods tournaient encore : maxUnavailable (25 %) a gardé l'ancien ReplicaSet.
