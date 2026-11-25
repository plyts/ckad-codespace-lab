# Préparation de m4-05 (CTX, NS, OUT fournis par le lanceur)
mkdir -p "$OUT" && cp -r "$ROOT/app/charts/webapp" "$OUT/webapp"
helm --kube-context "$CTX" -n "$NS" install wiki "$OUT/webapp" --wait --timeout 3m >/dev/null
