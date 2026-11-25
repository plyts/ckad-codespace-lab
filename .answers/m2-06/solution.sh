#!/usr/bin/env bash
# Solution de référence : m2-06 — CrashLoopBackOff : fichier manquant
kubectl config use-context ckad-a

kubectl -n m2-06 create configmap billing-config --from-literal=ready=yes
kubectl -n m2-06 patch deploy billing --type=json -p '[
  {"op":"add","path":"/spec/template/spec/volumes","value":[{"name":"cfg","configMap":{"name":"billing-config"}}]},
  {"op":"add","path":"/spec/template/spec/containers/0/volumeMounts","value":[{"name":"cfg","mountPath":"/config"}]}]'
kubectl -n m2-06 rollout status deploy/billing --timeout=120s
