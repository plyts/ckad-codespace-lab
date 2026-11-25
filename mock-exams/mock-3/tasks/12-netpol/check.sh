# Contrôles de m3-12 (sourcé après lib/check.sh)
ck_eq "podSelector app=ledger, type Ingress" "ledger Ingress" 'jp netpol ledger-access "{.spec.podSelector.matchLabels.app} {.spec.policyTypes[*]}"' \
  "La politique se pose sur la destination." "kubectl -n $NS describe netpol ledger-access"
ck_eq "Source role=accounting, port 80" "accounting 80" 'jp netpol ledger-access "{.spec.ingress[0].from[0].podSelector.matchLabels.role} {.spec.ingress[0].ports[0].port}"' \
  "ingress[0].from[0].podSelector et ingress[0].ports[0].port." "kubectl -n $NS get netpol ledger-access -o yaml"
ck_http "role=accounting passe" "$NS" "role=accounting" "http://ledger.$NS" "Welcome to nginx" "Le trafic autorisé doit passer." "kubectl -n $NS describe netpol"
ck_http_blocked "Les autres sont bloqués" "$NS" "app=intrus" "http://ledger.$NS" "Une politique Ingress sélectionnant un Pod refuse tout ce qu'elle ne liste pas." "kubectl -n $NS describe netpol"
