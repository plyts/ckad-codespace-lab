# Préparation de d3-06 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k run big --image=nginx:1.27-alpine --overrides='{"spec":{"containers":[{"name":"big","image":"nginx:1.27-alpine","resources":{"requests":{"cpu":"50"}}}]}}'
