#!/usr/bin/env bash
# Solution de référence : m4-10 — Secret en volume
kubectl config use-context ckad-a

kubectl -n m4-10 create secret generic smtp-creds --from-literal=user=app --from-literal=pass=Zx9-k2
kubectl -n m4-10 patch deploy mailer --type=json -p '[
  {"op":"add","path":"/spec/template/spec/volumes","value":[{"name":"creds","secret":{"secretName":"smtp-creds"}}]},
  {"op":"add","path":"/spec/template/spec/containers/0/volumeMounts","value":[{"name":"creds","mountPath":"/etc/creds","readOnly":true}]}]'
kubectl -n m4-10 rollout status deploy/mailer --timeout=120s
