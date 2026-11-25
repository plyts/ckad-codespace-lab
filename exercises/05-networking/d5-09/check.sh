# Contrôles de d5-09 (sourcé après lib/check.sh)
ck_eq "Service catalog 8080 → 5678" "8080 5678" 'jp svc catalog "{.spec.ports[0].port} {.spec.ports[0].targetPort}"' \
  "kubectl expose deploy catalog --port=8080 --target-port=5678." "kubectl -n $NS get svc catalog"
ck_eq "Ingress : hôte et chemin" "catalog.lab.local /catalog" 'jp ingress catalog "{.spec.rules[0].host} {.spec.rules[0].http.paths[0].path}"' \
  "--rule='catalog.lab.local/catalog*=catalog:8080'." "kubectl -n $NS describe ingress catalog"
ck_http "Via l'Ingress : catalog ok" "$NS" "" "--header=Host:catalog.lab.local http://traefik.traefik.svc/catalog" "catalog ok" \
  "Le trafic venant de Traefik doit passer (namespaceSelector traefik)." "kubectl -n $NS describe ingress catalog; kubectl -n $NS describe netpol"
ck_eq "NetworkPolicy : depuis le namespace traefik" "traefik" 'jp netpol catalog-from-ingress "{.spec.ingress[0].from[0].namespaceSelector.matchLabels.kubernetes\.io/metadata\.name}"' \
  "namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: traefik}}." "kubectl -n $NS get netpol catalog-from-ingress -o yaml"
ck_http_blocked "Accès direct au Service bloqué" "$NS" "app=tester" "http://catalog.$NS:8080" \
  "Seul Traefik doit atteindre les Pods catalog." "kubectl -n $NS describe netpol catalog-from-ingress"
