# Préparation de m3-09 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment collector --image=busybox:1.37 -- sh -c 'sleep 3600'
k rollout status deploy/collector --timeout=180s
