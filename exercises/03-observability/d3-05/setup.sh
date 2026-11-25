# Préparation de d3-05 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment cache --image=redis:7.4-alpinee
