#!/usr/bin/env bash
# Solution de référence : m4-05 — Mise à jour Helm
kubectl config use-context ckad-a

helm -n m4-05 upgrade wiki ~/ckad/m4-05/webapp --set replicaCount=2 --set message=maj
kubectl -n m4-05 rollout status deploy/wiki-webapp --timeout=120s
helm -n m4-05 history wiki > ~/ckad/m4-05/history.txt
# Retour arrière possible : helm -n m4-05 rollback wiki 1
