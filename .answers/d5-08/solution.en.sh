#!/usr/bin/env bash
# Reference solution: d5-08 — Broken Ingress
kubectl config use-context ckad-a
kubectl get ingressclass                      # traefik only
kubectl -n d5-08 get svc blog                 # port 80
kubectl -n d5-08 patch ingress blog --type=json -p '[
  {"op":"replace","path":"/spec/ingressClassName","value":"traefik"},
  {"op":"replace","path":"/spec/rules/0/http/paths/0/backend/service/port/number","value":80}]'
kubectl -n d5-08 get ingress blog
