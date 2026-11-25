#!/usr/bin/env bash
# Solution de référence : s5-pannes — Trois pannes à réparer
kubectl config use-context ckad-a
# 1. orders : CreateContainerConfigError (clé DB_HOST absente)
kubectl -n pannes patch cm orders-config --type=merge -p '{"data":{"DB_HOST":"db"}}'
kubectl -n pannes rollout restart deploy/orders
# 2. payments : sélecteur faux, aucun Endpoint
kubectl -n pannes patch svc payments -p '{"spec":{"selector":{"app":"payments"}}}'
# 3. uploads : StorageClass inexistante (fast) ; storageClassName est immuable
kubectl get storageclass
kubectl -n pannes get pvc uploads -o yaml > pvc.yaml
kubectl -n pannes get pod uploader -o yaml > uploader.yaml
kubectl -n pannes delete pod uploader --now
kubectl -n pannes delete pvc uploads
sed -i 's/storageClassName: fast/storageClassName: standard/' pvc.yaml
kubectl apply -f pvc.yaml
kubectl replace --force -f uploader.yaml
kubectl -n pannes wait --for=condition=Ready pod/uploader --timeout=120s
kubectl -n pannes rollout status deploy/orders --timeout=120s
