#!/usr/bin/env bash
# Reference solution: d3-09 — Exam-style: misconfigured probes
kubectl config use-context ckad-a
until kubectl -n d3-09 get events | grep -qi 'liveness probe failed'; do sleep 2; done
kubectl -n d3-09 get events --sort-by=.lastTimestamp | grep -i 'liveness probe failed' | tail -1 > ~/ckad/d3-09/cause.txt
cat ~/ckad/d3-09/cause.txt
kubectl -n d3-09 patch deploy orders --type=json -p '[
  {"op":"replace","path":"/spec/template/spec/containers/0/livenessProbe/httpGet/port","value":5678},
  {"op":"add","path":"/spec/template/spec/containers/0/startupProbe",
   "value":{"httpGet":{"path":"/","port":5678},"failureThreshold":10,"periodSeconds":2}}]'
kubectl -n d3-09 rollout status deploy/orders --timeout=120s
