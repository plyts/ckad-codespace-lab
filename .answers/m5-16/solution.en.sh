#!/usr/bin/env bash
# Reference solution: m5-16 — Ingress
kubectl config use-context ckad-a

kubectl -n m5-16 create ingress front-ing --class=traefik \
  --rule='m5.lab.local/*=front:80' --rule='m5.lab.local/api*=api:9090'
kubectl -n m5-16 describe ingress front-ing
