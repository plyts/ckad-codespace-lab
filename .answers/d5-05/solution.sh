#!/usr/bin/env bash
# Solution de référence : d5-05 — Ingress à deux chemins
kubectl config use-context ckad-a
kubectl -n d5-05 create ingress shop --class=traefik \
  --rule='shop.lab.local/*=front:80' \
  --rule='shop.lab.local/api*=api:8080'
kubectl -n d5-05 describe ingress shop
# Depuis le Codespace (port 8080 publié par kind) :
#   curl -H 'Host: shop.lab.local' http://localhost:8080/api
