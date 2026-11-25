# Contrôles de m5-14 (sourcé après lib/check.sh)
ck_eq "Type et ports" "ClusterIP 8080 5678" 'jp svc ranking-svc "{.spec.type} {.spec.ports[0].port} {.spec.ports[0].targetPort}"' \
  "kubectl expose deploy ranking --name=ranking-svc --type=ClusterIP --port=8080 --target-port=5678." "kubectl -n $NS get svc"
ck_http "Le Service répond" "$NS" "" "http://ranking-svc.$NS:8080" "ranking ok" "Sélecteur app=ranking, targetPort 5678." "kubectl -n $NS get endpointslices"
