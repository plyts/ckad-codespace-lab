# Préparation de m1-02 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment storefront --image=nginx:1.27-alpine --replicas=3
k rollout status deploy/storefront --timeout=120s
