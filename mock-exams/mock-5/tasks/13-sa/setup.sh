# Préparation de m5-13 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment ingest --image=busybox:1.37 -- sh -c 'sleep 3600'
k rollout status deploy/ingest --timeout=180s
