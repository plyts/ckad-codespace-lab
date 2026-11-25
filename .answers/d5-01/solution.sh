#!/usr/bin/env bash
# Solution de référence : d5-01 — Exposer un Deployment (ClusterIP)
kubectl config use-context ckad-a
kubectl -n d5-01 expose deploy web --name=web --port=80 --target-port=80
kubectl -n d5-01 get svc,endpointslices
kubectl -n d5-01 run t --rm -i --image=busybox:1.37 --restart=Never -- wget -qO- http://web | head -4
