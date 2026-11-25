# Préparation de m3-07 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment queue --image=redis:7.4-alpine-oups --replicas=2
