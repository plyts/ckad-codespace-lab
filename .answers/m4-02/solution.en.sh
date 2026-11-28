#!/usr/bin/env bash
# Reference solution: m4-02 — DaemonSet on every node
kubectl config use-context ckad-b

kubectl -n m4-02 create deployment log-agent --image=busybox:1.37 --dry-run=client -o yaml -- sh -c 'sleep 3600' > ds.yaml
yq -i '.kind = "DaemonSet" | del(.spec.replicas) | del(.spec.strategy) | del(.status)
       | .spec.template.spec.tolerations = [{"key":"node-role.kubernetes.io/control-plane","operator":"Exists","effect":"NoSchedule"}]' ds.yaml
kubectl apply -f ds.yaml
kubectl -n m4-02 rollout status ds/log-agent --timeout=120s
