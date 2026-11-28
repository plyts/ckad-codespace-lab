#!/usr/bin/env bash
# Reference solution: m5-06 — Blue/green
kubectl config use-context ckad-a

kubectl -n m5-06 patch svc profile -p '{"spec":{"selector":{"app":"profile","color":"green"}}}'
kubectl -n m5-06 scale deploy profile-blue --replicas=0
