# Contrôles de d2-07 (sourcé après lib/check.sh)
ck_eq "web-green : 2 réplicas prêts" "2" 'jp deploy web-green "{.status.readyReplicas}"' \
  "La nouvelle version doit être prête AVANT la bascule." "kubectl -n $NS get deploy,pods -L version"
ck_eq "Le Service sélectionne version=green" "green" 'jp svc web "{.spec.selector.version}"' \
  "La bascule blue/green se fait en changeant le sélecteur du Service." "kubectl -n $NS get svc web -o jsonpath='{.spec.selector}'"
ck_eq "web-blue conservé" "2" 'jp deploy web-blue "{.spec.replicas}"' \
  "Garder blue permet un retour arrière instantané." "kubectl -n $NS get deploy"
ck_http "Le Service web répond green" "$NS" "" "http://web" "^green" \
  "Le Service doit pointer sur les Pods green (port 80 vers 5678)." "kubectl -n $NS get endpointslices -l kubernetes.io/service-name=web -o wide"
