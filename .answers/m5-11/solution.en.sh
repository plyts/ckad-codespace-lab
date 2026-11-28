#!/usr/bin/env bash
# Reference solution: m5-11 — Resources
kubectl config use-context ckad-a

kubectl -n m5-11 set resources deploy render --requests=cpu=200m,memory=256Mi --limits=cpu=500m,memory=512Mi
kubectl -n m5-11 rollout status deploy/render --timeout=120s
# Wait until the old Pods (without resources) are gone before reading the QoS
until [ "$(kubectl -n m5-11 get pods -l app=render --no-headers | wc -l)" -eq 2 ]; do sleep 1; done
kubectl -n m5-11 get pod -l app=render -o jsonpath='{.items[0].status.qosClass}' > ~/ckad/m5-11/qos.txt
