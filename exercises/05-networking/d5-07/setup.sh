# Préparation de d5-07 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment web --image=nginx:1.27-alpine
k expose deploy web --port=80
kubectl --context "$CTX" -n d5-07-db create deployment db --image=nginx:1.27-alpine
kubectl --context "$CTX" -n d5-07-db expose deploy db --port=80
