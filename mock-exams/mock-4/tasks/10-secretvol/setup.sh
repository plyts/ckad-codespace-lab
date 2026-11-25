# Préparation de m4-10 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment mailer --image=busybox:1.37 -- sh -c 'sleep 3600'
k rollout status deploy/mailer --timeout=180s
