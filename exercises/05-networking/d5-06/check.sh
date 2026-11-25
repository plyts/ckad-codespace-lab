# Contrôles de d5-06 (sourcé après lib/check.sh)
ck_eq "default-deny : tous les Pods, Ingress" "{} Ingress" 'echo "$(jp netpol default-deny "{.spec.podSelector}") $(jp netpol default-deny "{.spec.policyTypes[*]}")"' \
  "podSelector: {} sélectionne tous les Pods ; policyTypes [Ingress] sans règle ingress = tout bloquer." "kubectl -n $NS describe netpol default-deny"
ck_eq "allow-frontend vise app=api" "api" 'jp netpol allow-frontend "{.spec.podSelector.matchLabels.app}"' \
  "La politique s'applique aux Pods sélectionnés par podSelector." "kubectl -n $NS describe netpol allow-frontend"
ck_eq "allow-frontend : depuis role=frontend, port 80" "frontend 80" 'jp netpol allow-frontend "{.spec.ingress[0].from[0].podSelector.matchLabels.role} {.spec.ingress[0].ports[0].port}"' \
  "ingress[].from[].podSelector et ingress[].ports[].port." "kubectl -n $NS get netpol allow-frontend -o yaml"
ck_http "Un Pod role=frontend accède à api" "$NS" "role=frontend" "http://api.$NS" "Welcome to nginx" \
  "Le trafic autorisé doit passer." "kubectl -n $NS describe netpol"
ck_http_blocked "Un autre Pod est bloqué" "$NS" "role=other" "http://api.$NS" \
  "Sans le label role=frontend, default-deny s'applique." "kubectl -n $NS describe netpol"
