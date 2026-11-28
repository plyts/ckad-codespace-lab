#!/usr/bin/env bash
# Reference solution: m3-07 — Image not found
kubectl config use-context ckad-a

until kubectl -n m3-07 get pods -l app=queue --no-headers | grep -qE 'ImagePullBackOff|ErrImagePull'; do sleep 2; done
kubectl -n m3-07 get pods -l app=queue --no-headers | grep -oE 'ImagePullBackOff|ErrImagePull' | head -1 > ~/ckad/m3-07/status.txt
c=$(kubectl -n m3-07 get deploy queue -o jsonpath='{.spec.template.spec.containers[0].name}')
kubectl -n m3-07 set image deploy/queue $c=redis:7.4-alpine
kubectl -n m3-07 rollout status deploy/queue --timeout=120s
