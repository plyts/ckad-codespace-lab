# Préparation de s6-panne-rbac (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create serviceaccount reporter
mkdir -p "$OUT"
# Erreur RÉELLE renvoyée par l'API server, enregistrée pour l'exercice
{ k get pods --as=system:serviceaccount:$NS:reporter 2>&1 || true
  k get configmaps --as=system:serviceaccount:$NS:reporter 2>&1 || true; } > "$OUT/forbidden.log"
