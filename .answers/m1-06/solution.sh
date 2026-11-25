#!/usr/bin/env bash
# Solution de référence : m1-06 — Service à réparer
kubectl config use-context ckad-a

kubectl -n m1-06 patch svc inventory --type=json -p '[
  {"op":"replace","path":"/spec/selector","value":{"app":"inventory","tier":"api"}},
  {"op":"replace","path":"/spec/ports/0/targetPort","value":5678}]'
until [ -n "$(kubectl -n m1-06 get endpointslices -l kubernetes.io/service-name=inventory -o jsonpath='{.items[*].endpoints[*].addresses[*]}')" ]; do sleep 1; done
kubectl -n m1-06 get endpointslices -l kubernetes.io/service-name=inventory \
  -o jsonpath='{.items[*].endpoints[*].addresses[*]}' > ~/ckad/m1-06/endpoints.txt
