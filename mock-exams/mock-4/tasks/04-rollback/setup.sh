# Préparation de m4-04 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create deployment sessions --image=redis:7.4-alpine --replicas=2
k rollout status deploy/sessions --timeout=120s
k set image deploy/sessions redis=redis:9.9-nexistepas
