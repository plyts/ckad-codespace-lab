# Préparation de m4-15 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment vault --image=nginx:1.27-alpine
k expose deploy vault --port=80
k rollout status deploy/vault --timeout=180s
