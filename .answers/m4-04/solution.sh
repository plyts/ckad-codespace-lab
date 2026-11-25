#!/usr/bin/env bash
# Solution de référence : m4-04 — Retour arrière
kubectl config use-context ckad-a

kubectl -n m4-04 rollout history deploy/sessions
echo 1 > ~/ckad/m4-04/revision.txt
kubectl -n m4-04 rollout undo deploy/sessions --to-revision=1
kubectl -n m4-04 rollout status deploy/sessions --timeout=120s
