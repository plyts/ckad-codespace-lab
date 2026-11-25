# Préparation de m3-06 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment legacy --image=nginx:1.27-alpine --replicas=2
k rollout status deploy/legacy --timeout=180s
