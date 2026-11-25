# Contrôles de m3-13 (sourcé après lib/check.sh)
ck_eq "Type et ports" "NodePort 80 5678" 'jp svc gateway-svc "{.spec.type} {.spec.ports[0].port} {.spec.ports[0].targetPort}"' \
  "kubectl expose deploy gateway --name=gateway-svc --type=NodePort --port=80 --target-port=5678." "kubectl -n $NS get svc"
ck_http "Le Service répond" "$NS" "" "http://gateway-svc.$NS:80" "gateway ok" "Sélecteur app=gateway, targetPort 5678." "kubectl -n $NS get endpointslices"

ck_eq "nodePort 30180" "30180" 'jp svc gateway-svc "{.spec.ports[0].nodePort}"' "Édite le Service ou écris le YAML." "kubectl -n $NS get svc gateway-svc -o yaml | grep nodePort"
