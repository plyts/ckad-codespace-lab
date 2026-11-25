#!/usr/bin/env bash
# Solution de référence : d3-07 — API dépréciées : migrer un manifeste
kubectl config use-context ckad-a
kubectl apply -f ~/ckad/d3-07/old.yaml || true    # no matches for kind "CronJob" in version "batch/v1beta1"
kubectl api-resources | grep -E 'cronjobs|poddisruptionbudgets'   # batch/v1 et policy/v1
sed -i 's#batch/v1beta1#batch/v1#; s#policy/v1beta1#policy/v1#' ~/ckad/d3-07/old.yaml
kubectl apply -f ~/ckad/d3-07/old.yaml
# Aide officielle : https://kubernetes.io/docs/reference/using-api/deprecation-guide/
# Le plugin kubectl-convert existe mais n'est pas installé à l'examen.
