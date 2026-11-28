#!/usr/bin/env bash
# Reference solution: m4-14 — Ingress
kubectl config use-context ckad-b

kubectl -n m4-14 create ingress shop-ing --class=traefik \
  --rule='m4.lab.local/*=shop:80' --rule='m4.lab.local/cart*=cart:9090'
kubectl -n m4-14 describe ingress shop-ing
