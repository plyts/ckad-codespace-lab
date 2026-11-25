# Contrôles de d5-01 (sourcé après lib/check.sh)
ck_eq "Service web de type ClusterIP" "ClusterIP" 'jp svc web "{.spec.type}"' \
  "kubectl expose crée un ClusterIP par défaut." "kubectl -n $NS get svc"
ck_eq "Port 80 → 80" "80 80" 'jp svc web "{.spec.ports[0].port} {.spec.ports[0].targetPort}"' \
  "port = port du Service ; targetPort = port du conteneur." "kubectl -n $NS describe svc web"
ck_eq "2 Endpoints prêts" "2" 'kn get endpointslices -l kubernetes.io/service-name=web -o jsonpath="{range .items[*].endpoints[*]}{.conditions.ready}{\" \"}{end}" | grep -o true | wc -l | tr -d " "' \
  "Le sélecteur du Service doit correspondre aux labels des Pods (app=web)." "kubectl -n $NS get endpointslices -l kubernetes.io/service-name=web"
ck_http "http://web.$NS répond" "$NS" "" "http://web.$NS" "Welcome to nginx" \
  "Nom DNS court du Service dans le même namespace : web ; complet : web.$NS.svc.cluster.local." "kubectl -n $NS get svc web -o wide"
