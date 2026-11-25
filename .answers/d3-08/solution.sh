#!/usr/bin/env bash
# Solution de référence : d3-08 — kubectl top : le Pod le plus gourmand
kubectl config use-context ckad-a
for i in $(seq 30); do kubectl -n d3-08 top pods >/dev/null 2>&1 && break; sleep 5; done
kubectl -n d3-08 top pods --sort-by=cpu
kubectl -n d3-08 top pods --sort-by=cpu --no-headers | head -1 | awk '{print $1}' > ~/ckad/d3-08/top.txt
