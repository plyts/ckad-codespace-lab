#!/usr/bin/env bash
# Reference solution: m3-05 — Blue/green switch
kubectl config use-context ckad-b

kubectl -n m3-05 patch svc checkout -p '{"spec":{"selector":{"app":"checkout","color":"green"}}}'
kubectl -n m3-05 scale deploy checkout-blue --replicas=0
