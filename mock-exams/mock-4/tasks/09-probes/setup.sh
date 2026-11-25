# Préparation de m4-09 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment media --image=nginx:1.27-alpine --replicas=2
k rollout status deploy/media --timeout=180s
