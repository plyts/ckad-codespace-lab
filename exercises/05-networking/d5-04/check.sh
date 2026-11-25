# Contrôles de d5-04 (sourcé après lib/check.sh)
ck_eq "Sélecteur app=shop" "shop" 'jp svc shop "{.spec.selector.app}"' \
  "Le sélecteur (app=shopp) ne correspond à aucun Pod : Service sans Endpoints." "kubectl -n $NS get pods --show-labels; kubectl -n $NS get endpointslices"
ck_eq "targetPort 5678" "5678" 'jp svc shop "{.spec.ports[0].targetPort}"' \
  "http-echo écoute sur 5678 : un mauvais targetPort donne Connection refused." "kubectl -n $NS get pod -l app=shop -o jsonpath='{.items[0].spec.containers[0].ports}'"
ck_eq "Deployment inchangé (2 réplicas app=shop)" "2 shop" 'jp deploy shop "{.status.readyReplicas} {.spec.template.metadata.labels.app}"' \
  "La consigne impose de corriger le Service." "kubectl -n $NS get deploy shop -o wide"
ck_http "http://shop.$NS répond « shop ok »" "$NS" "" "http://shop.$NS" "shop ok" \
  "Sélecteur ET port cible doivent être justes." "kubectl -n $NS describe svc shop"
