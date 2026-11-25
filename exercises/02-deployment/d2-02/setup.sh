# Préparation de d2-02 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment front --image=nginx:1.27-alpine --replicas=1
