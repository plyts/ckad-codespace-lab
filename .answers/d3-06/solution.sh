#!/usr/bin/env bash
# Solution de référence : d3-06 — Pod Pending : lire les événements
kubectl config use-context ckad-a
kubectl -n d3-06 get events --field-selector involvedObject.name=big     # REASON = FailedScheduling
echo FailedScheduling > ~/ckad/d3-06/reason.txt
kubectl -n d3-06 get pod big -o yaml > big.yaml
sed -i 's/cpu: "50"/cpu: 50m/' big.yaml
kubectl replace --force -f big.yaml          # supprime puis recrée le Pod
kubectl -n d3-06 wait --for=condition=Ready pod/big --timeout=90s
