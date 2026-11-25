#!/usr/bin/env bash
# Solution de référence : m1-03 — Sondes readiness et liveness
kubectl config use-context ckad-a

kubectl -n m1-03 patch deploy catalog --type=json -p '[
  {"op":"add","path":"/spec/template/spec/containers/0/readinessProbe","value":{"httpGet":{"path":"/index.html","port":80},"periodSeconds":5}},
  {"op":"add","path":"/spec/template/spec/containers/0/livenessProbe","value":{"tcpSocket":{"port":80},"initialDelaySeconds":10,"periodSeconds":15}}]'
kubectl -n m1-03 rollout status deploy/catalog --timeout=120s
