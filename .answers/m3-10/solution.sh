#!/usr/bin/env bash
# Solution de référence : m3-10 — Ressources et QoS
kubectl config use-context ckad-a

kubectl -n m3-10 set resources deploy api --requests=cpu=100m,memory=128Mi --limits=cpu=100m,memory=128Mi
kubectl -n m3-10 rollout status deploy/api --timeout=120s
# Attendre que les anciens Pods (sans ressources) aient disparu avant de lire la QoS
until [ "$(kubectl -n m3-10 get pods -l app=api --no-headers | wc -l)" -eq 2 ]; do sleep 1; done
kubectl -n m3-10 get pod -l app=api -o jsonpath='{.items[0].status.qosClass}' > ~/ckad/m3-10/qos.txt
