# Contrôles de m4-16 (sourcé après lib/check.sh)
ck_http "Le Service répond" "$NS" "" "http://orders.$NS" "orders ok" \
  "Deux erreurs : tier=backend n'existe pas sur les Pods (tier=api) et targetPort 8080 au lieu de 5678." "kubectl -n $NS get pods --show-labels; kubectl -n $NS describe svc orders"
ck_true "endpoints.txt contient les IP des Pods" "( ips=\$(kubectl --context $CTX -n $NS get pods -l app=orders -o jsonpath='{.items[*].status.podIP}'); [ -n \"\$ips\" ] || exit 1; for ip in \$ips; do grep -q \$ip $OUT/endpoints.txt || exit 1; done )" \
  "kubectl get endpointslices -l kubernetes.io/service-name=orders -o wide." "cat $OUT/endpoints.txt"
