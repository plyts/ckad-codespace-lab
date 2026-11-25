# Préparation de s4-jour4 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k apply -f "$ROOT/app/boutique/jour2.yaml"
for d in redis api front; do k rollout status deploy/$d --timeout=180s; done
