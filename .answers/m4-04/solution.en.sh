#!/usr/bin/env bash
# Reference solution: m4-04 — Rollback
kubectl config use-context ckad-a

kubectl -n m4-04 rollout history deploy/sessions
echo 1 > ~/ckad/m4-04/revision.txt
kubectl -n m4-04 rollout undo deploy/sessions --to-revision=1
kubectl -n m4-04 rollout status deploy/sessions --timeout=120s
