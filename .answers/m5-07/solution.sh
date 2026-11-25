#!/usr/bin/env bash
# Solution de référence : m5-07 — CrashLoopBackOff
kubectl config use-context ckad-b

kubectl -n m5-07 create configmap notifier-config --from-literal=ready=yes
kubectl -n m5-07 patch deploy notifier --type=json -p '[
  {"op":"add","path":"/spec/template/spec/volumes","value":[{"name":"cfg","configMap":{"name":"notifier-config"}}]},
  {"op":"add","path":"/spec/template/spec/containers/0/volumeMounts","value":[{"name":"cfg","mountPath":"/config"}]}]'
kubectl -n m5-07 rollout status deploy/notifier --timeout=120s
