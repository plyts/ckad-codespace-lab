#!/usr/bin/env bash
# Solution de référence : m2-05 — Extraire une erreur des logs
kubectl config use-context ckad-b

kubectl -n m2-05 wait --for=condition=Ready pod/ingestor --timeout=60s
kubectl -n m2-05 logs ingestor | grep ERROR > ~/ckad/m2-05/error.txt
