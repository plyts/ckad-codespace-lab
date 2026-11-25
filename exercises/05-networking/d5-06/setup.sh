# Préparation de d5-06 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment api --image=nginx:1.27-alpine
k expose deploy api --port=80
