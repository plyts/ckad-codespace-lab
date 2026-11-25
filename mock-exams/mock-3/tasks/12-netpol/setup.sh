# Préparation de m3-12 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment ledger --image=nginx:1.27-alpine
k expose deploy ledger --port=80
k rollout status deploy/ledger --timeout=180s
