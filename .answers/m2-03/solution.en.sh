#!/usr/bin/env bash
# Reference solution: m2-03 — Helm upgrade
kubectl config use-context ckad-b

helm -n m2-03 upgrade blog ~/ckad/m2-03/webapp --set replicaCount=3 --set message=v2
kubectl -n m2-03 rollout status deploy/blog-webapp --timeout=120s
helm -n m2-03 history blog > ~/ckad/m2-03/history.txt
# Possible rollback: helm -n m2-03 rollback blog 1
