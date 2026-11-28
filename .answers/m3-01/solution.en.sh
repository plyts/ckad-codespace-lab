#!/usr/bin/env bash
# Reference solution: m3-01 — Parallel Job
kubectl config use-context ckad-a

kubectl -n m3-01 create job resize --image=busybox:1.37 --dry-run=client -o yaml -- sh -c 'echo redimensionné' > resize.yaml
yq -i '.spec.completions = 4 | .spec.parallelism = 2 | .spec.backoffLimit = 1' resize.yaml
kubectl apply -f resize.yaml
kubectl -n m3-01 wait --for=condition=Complete job/resize --timeout=180s
