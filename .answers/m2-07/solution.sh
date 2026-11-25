#!/usr/bin/env bash
# Solution de référence : m2-07 — Droits d'un ServiceAccount
kubectl config use-context ckad-b

kubectl -n m2-07 create serviceaccount auditor
kubectl -n m2-07 create role auditor-role --verb=get,list,watch --resource=deployments,pods
kubectl -n m2-07 create rolebinding auditor-binding --role=auditor-role --serviceaccount=m2-07:auditor
kubectl auth can-i --list -n m2-07 --as=system:serviceaccount:m2-07:auditor | head
