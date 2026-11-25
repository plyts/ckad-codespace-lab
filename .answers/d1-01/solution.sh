#!/usr/bin/env bash
# Solution de référence : d1-01 — Premier Pod nginx
kubectl config use-context ckad-a
# Impératif : le plus rapide à l'examen.
kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80
kubectl -n d1-01 wait --for=condition=Ready pod/web --timeout=90s
# Vérification à la main :
kubectl -n d1-01 get pod web --show-labels -o wide
# VARIANTE : générer le YAML puis l'appliquer
#   kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80 --dry-run=client -o yaml > web.yaml
#   kubectl apply -f web.yaml
