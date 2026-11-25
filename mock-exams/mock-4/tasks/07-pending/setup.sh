# Préparation de m4-07 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k run batch --image=nginx:1.27-alpine --overrides='{"spec":{"nodeSelector":{"disk":"ssd"},"containers":[{"name":"batch","image":"nginx:1.27-alpine"}]}}'
