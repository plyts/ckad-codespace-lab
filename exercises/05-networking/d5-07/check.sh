# Contrôles de d5-07 (sourcé après lib/check.sh)
ck_eq "client-egress vise app=client, type Egress" "client Egress" 'jp netpol client-egress "{.spec.podSelector.matchLabels.app} {.spec.policyTypes[*]}"' \
  "policyTypes: [Egress] et podSelector app=client." "kubectl -n $NS describe netpol client-egress"
ck_match "Destination : namespace d5-07-db ET Pods app=db" "d5-07-db.*db|db.*d5-07-db" 'jp netpol client-egress "{.spec.egress[*].to[*].namespaceSelector.matchLabels} {.spec.egress[*].to[*].podSelector.matchLabels}"' \
  "namespaceSelector (kubernetes.io/metadata.name: d5-07-db) et podSelector dans le MÊME élément to (ET), pas deux éléments (OU)." "kubectl -n $NS get netpol client-egress -o yaml"
ck_match "DNS autorisé (port 53)" "53" 'jp netpol client-egress "{.spec.egress[*].ports[*].port}"' \
  "Sans DNS, le nom db.d5-07-db ne se résout plus : la sortie vers 53/UDP et 53/TCP doit être permise." "kubectl -n $NS get netpol client-egress -o yaml"
ck_http "app=client atteint db.d5-07-db" "$NS" "app=client" "http://db.d5-07-db" "Welcome to nginx" \
  "DNS + destination db doivent être autorisés." "kubectl -n $NS describe netpol client-egress"
ck_http_blocked "app=client ne peut pas joindre web.d5-07" "$NS" "app=client" "http://web.$NS" \
  "Une fois Egress dans policyTypes, tout ce qui n'est pas listé est bloqué." "kubectl -n $NS describe netpol client-egress"
