#!/usr/bin/env bash
# Solution de référence : m4-16 — Service à réparer
kubectl config use-context ckad-a

kubectl -n m4-16 patch svc orders --type=json -p '[
  {"op":"replace","path":"/spec/selector","value":{"app":"orders","tier":"api"}},
  {"op":"replace","path":"/spec/ports/0/targetPort","value":5678}]'
until [ -n "$(kubectl -n m4-16 get endpointslices -l kubernetes.io/service-name=orders -o jsonpath='{.items[*].endpoints[*].addresses[*]}')" ]; do sleep 1; done
kubectl -n m4-16 get endpointslices -l kubernetes.io/service-name=orders \
  -o jsonpath='{.items[*].endpoints[*].addresses[*]}' > ~/ckad/m4-16/endpoints.txt
