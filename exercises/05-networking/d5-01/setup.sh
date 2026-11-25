# Préparation de d5-01 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment web --image=nginx:1.27-alpine --replicas=2
