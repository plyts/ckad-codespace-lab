# Préparation de d2-05 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment api --image=hashicorp/http-echo:1.0.0 --replicas=2 -- /http-echo -text=api
