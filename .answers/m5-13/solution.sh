#!/usr/bin/env bash
# Solution de référence : m5-13 — ServiceAccount
kubectl config use-context ckad-a

kubectl -n m5-13 create serviceaccount uploader
kubectl -n m5-13 set serviceaccount deploy/ingest uploader
kubectl -n m5-13 rollout status deploy/ingest --timeout=120s
