#!/usr/bin/env bash
# Reference solution: d3-01 — Find a line in the logs
kubectl config use-context ckad-a
kubectl -n d3-01 wait --for=condition=Ready pod/talker --timeout=60s
kubectl -n d3-01 logs talker | grep SECRET_CODE | cut -d= -f2 > ~/ckad/d3-01/code.txt
cat ~/ckad/d3-01/code.txt
# Useful kubectl logs options: --tail=20, -f, --since=5m, -c <container>, --previous, -l app=x
