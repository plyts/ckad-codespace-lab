# Préparation de m1-03 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment catalog --image=nginx:1.27-alpine --replicas=2
k rollout status deploy/catalog --timeout=180s
