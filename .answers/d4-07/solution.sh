#!/usr/bin/env bash
# Solution de référence : d4-07 — RBAC : Role et RoleBinding
kubectl config use-context ckad-a
kubectl -n d4-07 create role pod-reader --verb=get,list,watch --resource=pods,pods/log
kubectl -n d4-07 create rolebinding monitor-pod-reader --role=pod-reader --serviceaccount=d4-07:monitor
kubectl auth can-i list pods -n d4-07 --as=system:serviceaccount:d4-07:monitor     # yes
kubectl auth can-i delete pods -n d4-07 --as=system:serviceaccount:d4-07:monitor || true  # no (code retour 1)
