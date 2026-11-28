#!/usr/bin/env bash
# Reference solution: d5-05 — Ingress with two paths
kubectl config use-context ckad-a
kubectl -n d5-05 create ingress shop --class=traefik \
  --rule='shop.lab.local/*=front:80' \
  --rule='shop.lab.local/api*=api:8080'
kubectl -n d5-05 describe ingress shop
# From the Codespace (port 8080 published by kind):
#   curl -H 'Host: shop.lab.local' http://localhost:8080/api
