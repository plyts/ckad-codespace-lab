#!/usr/bin/env bash
# Solution de référence : m1-02 — Mise à jour avec motif
kubectl config use-context ckad-a

kubectl -n m1-02 set image deploy/storefront nginx=nginx:1.28-alpine
kubectl -n m1-02 annotate deploy storefront kubernetes.io/change-cause='nginx 1.28'
kubectl -n m1-02 scale deploy storefront --replicas=4
kubectl -n m1-02 rollout status deploy/storefront --timeout=120s
