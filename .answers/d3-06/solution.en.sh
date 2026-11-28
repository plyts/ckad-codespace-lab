#!/usr/bin/env bash
# Reference solution: d3-06 — Pending Pod: read the events
kubectl config use-context ckad-a
kubectl -n d3-06 get events --field-selector involvedObject.name=big     # REASON = FailedScheduling
echo FailedScheduling > ~/ckad/d3-06/reason.txt
kubectl -n d3-06 get pod big -o yaml > big.yaml
sed -i 's/cpu: "50"/cpu: 50m/' big.yaml
kubectl replace --force -f big.yaml          # deletes then recreates the Pod
kubectl -n d3-06 wait --for=condition=Ready pod/big --timeout=90s
