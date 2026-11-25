#!/usr/bin/env bash
# Solution de référence : s2-jour2 — Boutique, journée 2 : configuration et montée en charge
kubectl config use-context ckad-a
kubectl -n boutique-j2 create configmap front-html --from-literal=index.html='Boutique jour 2'
kubectl -n boutique-j2 patch deploy front --type=json -p '[
  {"op":"add","path":"/spec/template/spec/volumes","value":[{"name":"html","configMap":{"name":"front-html"}}]},
  {"op":"add","path":"/spec/template/spec/containers/0/volumeMounts","value":[{"name":"html","mountPath":"/usr/share/nginx/html"}]}]'
kubectl -n boutique-j2 create secret generic redis-auth --from-literal=password=r3d1s-pass
kubectl -n boutique-j2 set env deploy/api --from=secret/redis-auth --prefix=REDIS_
kubectl -n boutique-j2 set resources deploy api --requests=cpu=50m,memory=32Mi --limits=cpu=100m,memory=64Mi
kubectl -n boutique-j2 scale deploy api --replicas=3
for d in front api; do kubectl -n boutique-j2 rollout status deploy/$d --timeout=180s; done
# Référence déclarative : app/boutique/jour2.yaml
