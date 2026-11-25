# Préparation de m5-11 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment render --image=nginx:1.27-alpine --replicas=2
k rollout status deploy/render --timeout=180s
