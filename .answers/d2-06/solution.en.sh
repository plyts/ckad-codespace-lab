#!/usr/bin/env bash
# Reference solution: d2-06 — Install a Helm chart
kubectl config use-context ckad-a
helm show values ~/ckad/d2-06/webapp > ~/ckad/d2-06/values.txt
helm -n d2-06 install shop ~/ckad/d2-06/webapp --set replicaCount=2 --set image.tag=1.28-alpine
kubectl -n d2-06 rollout status deploy/shop-webapp --timeout=120s
helm -n d2-06 list
# Other useful commands: helm upgrade, helm rollback shop 1, helm uninstall shop, helm get values shop
