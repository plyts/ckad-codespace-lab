# Préparation de m5-15 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment secrets-api --image=nginx:1.27-alpine
k expose deploy secrets-api --port=80
k rollout status deploy/secrets-api --timeout=180s
