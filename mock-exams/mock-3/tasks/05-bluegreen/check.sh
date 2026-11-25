# Contrôles de m3-05 (sourcé après lib/check.sh)
ck_eq "Sélecteur color=green" "green" 'jp svc checkout "{.spec.selector.color}"' "Changer le sélecteur du Service." "kubectl -n $NS get svc checkout -o jsonpath='{.spec.selector}'"
ck_eq "checkout-blue à 0, conservé" "0" 'jp deploy checkout-blue "{.spec.replicas}"' "kubectl scale --replicas=0 garde le Deployment." "kubectl -n $NS get deploy"
ck_http "Le Service répond green" "$NS" "" "http://checkout.$NS" "^green" "Le Service doit viser les Pods green." "kubectl -n $NS get endpointslices"
