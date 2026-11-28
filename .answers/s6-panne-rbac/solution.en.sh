#!/usr/bin/env bash
# Reference solution: s6-panne-rbac — Forbidden: repair a ServiceAccount's permissions
kubectl config use-context ckad-a
cat ~/ckad/s6-panne-rbac/forbidden.log
kubectl -n rapports create role reporter --verb=get,list --resource=pods,configmaps
kubectl -n rapports create rolebinding reporter --role=reporter --serviceaccount=rapports:reporter
kubectl auth can-i list configmaps -n rapports --as=system:serviceaccount:rapports:reporter
