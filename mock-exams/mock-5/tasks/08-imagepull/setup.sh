# Préparation de m5-08 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment frontend --image=nginx:1.27-alpine3 --replicas=2
