# Contrôles de m4-15 (sourcé après lib/check.sh)
ck_eq "namespaceSelector m4-15-ops" "m4-15-ops" 'jp netpol from-m4-15-ops "{.spec.ingress[0].from[0].namespaceSelector.matchLabels.kubernetes\.io/metadata\.name}"' \
  "Label automatique kubernetes.io/metadata.name=m4-15-ops." "kubectl get ns m4-15-ops --show-labels"
ck_http "Depuis m4-15-ops : OK" "m4-15-ops" "" "http://vault.$NS" "Welcome to nginx" "Le namespace m4-15-ops doit passer." "kubectl -n $NS describe netpol"
ck_http_blocked "Depuis m4-15 : bloqué" "$NS" "" "http://vault.$NS" "Même le namespace local est refusé." "kubectl -n $NS describe netpol"
