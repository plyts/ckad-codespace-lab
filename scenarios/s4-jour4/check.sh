# Contrôles de s4-jour4 (sourcé après lib/check.sh)
ck_eq "default-deny" "{} Ingress" 'echo "$(jp netpol default-deny "{.spec.podSelector}") $(jp netpol default-deny "{.spec.policyTypes[*]}")"' \
  "podSelector: {} + policyTypes: [Ingress], sans règle." "kubectl -n $NS get netpol"
ck_eq "front-to-api" "api front 5678" 'jp netpol front-to-api "{.spec.podSelector.matchLabels.app} {.spec.ingress[0].from[0].podSelector.matchLabels.app} {.spec.ingress[0].ports[0].port}"' \
  "La politique se pose sur la DESTINATION (api) et autorise la source (front)." "kubectl -n $NS describe netpol front-to-api"
ck_eq "api-to-redis" "redis api 6379" 'jp netpol api-to-redis "{.spec.podSelector.matchLabels.app} {.spec.ingress[0].from[0].podSelector.matchLabels.app} {.spec.ingress[0].ports[0].port}"' \
  "Destination redis, source api, port 6379." "kubectl -n $NS describe netpol api-to-redis"
ck_http "Via l'Ingress : la boutique répond" "$NS" "" "--header=Host:boutique.lab.local http://traefik.traefik.svc/" "Boutique jour 2" \
  "Ingress boutique ET NetworkPolicy ingress-to-front (namespaceSelector traefik)." "kubectl -n $NS describe ingress boutique; kubectl -n $NS describe netpol ingress-to-front"
ck_http "front joint l'API" "$NS" "app=front" "http://api.$NS" "api v1" \
  "front-to-api doit autoriser le port du conteneur (5678), pas celui du Service." "kubectl -n $NS describe netpol front-to-api"
ck_http_blocked "front ne joint pas Redis" "$NS" "app=front" "http://redis.$NS:6379" \
  "Seul api-to-redis ouvre Redis, et seulement aux Pods app=api." "kubectl -n $NS describe netpol"
