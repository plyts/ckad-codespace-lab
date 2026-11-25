#!/usr/bin/env bash
# Solution de référence : m4-09 — Sondes
kubectl config use-context ckad-b

kubectl -n m4-09 patch deploy media --type=json -p '[
  {"op":"add","path":"/spec/template/spec/containers/0/readinessProbe","value":{"httpGet":{"path":"/","port":80},"periodSeconds":5}},
  {"op":"add","path":"/spec/template/spec/containers/0/livenessProbe","value":{"tcpSocket":{"port":80},"initialDelaySeconds":10,"periodSeconds":15}}]'
kubectl -n m4-09 rollout status deploy/media --timeout=120s
