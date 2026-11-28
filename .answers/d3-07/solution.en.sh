#!/usr/bin/env bash
# Reference solution: d3-07 — Deprecated APIs: migrate a manifest
kubectl config use-context ckad-a
kubectl apply -f ~/ckad/d3-07/old.yaml || true    # no matches for kind "CronJob" in version "batch/v1beta1"
kubectl api-resources | grep -E 'cronjobs|poddisruptionbudgets'   # batch/v1 and policy/v1
sed -i 's#batch/v1beta1#batch/v1#; s#policy/v1beta1#policy/v1#' ~/ckad/d3-07/old.yaml
kubectl apply -f ~/ckad/d3-07/old.yaml
# Official help: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
# The kubectl-convert plugin exists but is not installed in the exam.
