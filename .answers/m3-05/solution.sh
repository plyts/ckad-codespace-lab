#!/usr/bin/env bash
# Solution de référence : m3-05 — Bascule blue/green
kubectl config use-context ckad-b

kubectl -n m3-05 patch svc checkout -p '{"spec":{"selector":{"app":"checkout","color":"green"}}}'
kubectl -n m3-05 scale deploy checkout-blue --replicas=0
