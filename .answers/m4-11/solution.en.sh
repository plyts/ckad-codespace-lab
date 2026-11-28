#!/usr/bin/env bash
# Reference solution: m4-11 — RBAC
kubectl config use-context ckad-a

kubectl -n m4-11 create serviceaccount deployer
kubectl -n m4-11 create role deployer-role --verb=get,list,create,update --resource=deployments
kubectl -n m4-11 create rolebinding deployer-binding --role=deployer-role --serviceaccount=m4-11:deployer
kubectl auth can-i --list -n m4-11 --as=system:serviceaccount:m4-11:deployer | head
