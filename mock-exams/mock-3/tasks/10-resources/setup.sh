# Préparation de m3-10 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment api --image=nginx:1.27-alpine --replicas=2
k rollout status deploy/api --timeout=180s
