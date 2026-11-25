#!/usr/bin/env bash
# Solution de référence : m5-01 — Job à complétions
kubectl config use-context ckad-b

kubectl -n m5-01 create job migrate --image=busybox:1.37 --dry-run=client -o yaml -- sh -c 'echo migré' > migrate.yaml
yq -i '.spec.completions = 3 | .spec.parallelism = 1 | .spec.backoffLimit = 1' migrate.yaml
kubectl apply -f migrate.yaml
kubectl -n m5-01 wait --for=condition=Complete job/migrate --timeout=180s
