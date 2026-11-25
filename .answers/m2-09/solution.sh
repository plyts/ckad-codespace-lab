#!/usr/bin/env bash
# Solution de référence : m2-09 — Ingress à deux chemins
kubectl config use-context ckad-a

kubectl -n m2-09 create ingress home-ing --class=traefik \
  --rule='m2.lab.local/*=home:80' --rule='m2.lab.local/docs*=docs:9090'
kubectl -n m2-09 describe ingress home-ing
