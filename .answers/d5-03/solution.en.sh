#!/usr/bin/env bash
# Reference solution: d5-03 — Service DNS
kubectl config use-context ckad-a
echo db.d5-03.svc.cluster.local > ~/ckad/d5-03/fqdn.txt
kubectl -n d5-03 get svc db -o jsonpath='{.spec.clusterIP}' > ~/ckad/d5-03/ip.txt
kubectl -n d5-03 run t --rm -i --image=busybox:1.37 --restart=Never -- nslookup db.d5-03.svc.cluster.local
