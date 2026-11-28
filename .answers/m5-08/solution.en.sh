#!/usr/bin/env bash
# Reference solution: m5-08 — ImagePullBackOff
kubectl config use-context ckad-a

until kubectl -n m5-08 get pods -l app=frontend --no-headers | grep -qE 'ImagePullBackOff|ErrImagePull'; do sleep 2; done
kubectl -n m5-08 get pods -l app=frontend --no-headers | grep -oE 'ImagePullBackOff|ErrImagePull' | head -1 > ~/ckad/m5-08/status.txt
c=$(kubectl -n m5-08 get deploy frontend -o jsonpath='{.spec.template.spec.containers[0].name}')
kubectl -n m5-08 set image deploy/frontend $c=nginx:1.27-alpine
kubectl -n m5-08 rollout status deploy/frontend --timeout=120s
