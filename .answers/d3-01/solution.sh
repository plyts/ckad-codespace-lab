#!/usr/bin/env bash
# Solution de référence : d3-01 — Trouver une ligne dans les logs
kubectl config use-context ckad-a
kubectl -n d3-01 wait --for=condition=Ready pod/talker --timeout=60s
kubectl -n d3-01 logs talker | grep SECRET_CODE | cut -d= -f2 > ~/ckad/d3-01/code.txt
cat ~/ckad/d3-01/code.txt
# Options utiles de kubectl logs : --tail=20, -f, --since=5m, -c <conteneur>, --previous, -l app=x
