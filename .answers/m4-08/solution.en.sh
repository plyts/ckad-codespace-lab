#!/usr/bin/env bash
# Reference solution: m4-08 — Logs
kubectl config use-context ckad-a

kubectl -n m4-08 wait --for=condition=Ready pod/sync --timeout=60s
kubectl -n m4-08 logs sync | grep ERROR > ~/ckad/m4-08/error.txt
