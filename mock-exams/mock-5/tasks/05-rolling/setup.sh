# Préparation de m5-05 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment portal --image=nginx:1.27-alpine --replicas=3
k rollout status deploy/portal --timeout=120s
