# Préparation de m2-03 (CTX, NS, OUT fournis par le lanceur)
mkdir -p "$OUT" && cp -r "$ROOT/app/charts/webapp" "$OUT/webapp"
helm --kube-context "$CTX" -n "$NS" install blog "$OUT/webapp" --wait --timeout 3m >/dev/null
