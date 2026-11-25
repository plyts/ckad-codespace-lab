#!/usr/bin/env bash
# Solution de référence : d5-04 — Service sans Endpoints
kubectl config use-context ckad-a
kubectl -n d5-04 get endpointslices -l kubernetes.io/service-name=shop     # aucun endpoint
kubectl -n d5-04 get pods --show-labels                                   # app=shop
kubectl -n d5-04 patch svc shop --type=json -p '[
  {"op":"replace","path":"/spec/selector","value":{"app":"shop"}},
  {"op":"replace","path":"/spec/ports/0/targetPort","value":5678}]'
kubectl -n d5-04 get endpointslices -l kubernetes.io/service-name=shop
