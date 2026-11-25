# Contrôles de m5-15 (sourcé après lib/check.sh)
ck_eq "podSelector app=secrets-api, type Ingress" "secrets-api Ingress" 'jp netpol secrets-api-access "{.spec.podSelector.matchLabels.app} {.spec.policyTypes[*]}"' \
  "La politique se pose sur la destination." "kubectl -n $NS describe netpol secrets-api-access"
ck_eq "Source access=granted, port 80" "granted 80" 'jp netpol secrets-api-access "{.spec.ingress[0].from[0].podSelector.matchLabels.access} {.spec.ingress[0].ports[0].port}"' \
  "ingress[0].from[0].podSelector et ingress[0].ports[0].port." "kubectl -n $NS get netpol secrets-api-access -o yaml"
ck_http "access=granted passe" "$NS" "access=granted" "http://secrets-api.$NS" "Welcome to nginx" "Le trafic autorisé doit passer." "kubectl -n $NS describe netpol"
ck_http_blocked "Les autres sont bloqués" "$NS" "app=intrus" "http://secrets-api.$NS" "Une politique Ingress sélectionnant un Pod refuse tout ce qu'elle ne liste pas." "kubectl -n $NS describe netpol"
