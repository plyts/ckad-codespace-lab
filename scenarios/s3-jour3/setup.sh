# Préparation de s3-jour3 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k apply -f "$ROOT/app/boutique/jour2.yaml"
for d in redis api front; do k rollout status deploy/$d --timeout=180s; done

k annotate deploy api kubernetes.io/change-cause="v1 stable" --overwrite
k patch deploy api --type=json -p '[{"op":"replace","path":"/spec/template/spec/containers/0/args","value":["-text=api v2","-timeout=oups"]}]'
k annotate deploy api kubernetes.io/change-cause="v2" --overwrite
