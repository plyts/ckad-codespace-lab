# Contrôles de m5-06 (sourcé après lib/check.sh)
ck_eq "Sélecteur color=green" "green" 'jp svc profile "{.spec.selector.color}"' "Changer le sélecteur du Service." "kubectl -n $NS get svc profile -o jsonpath='{.spec.selector}'"
ck_eq "profile-blue à 0, conservé" "0" 'jp deploy profile-blue "{.spec.replicas}"' "kubectl scale --replicas=0 garde le Deployment." "kubectl -n $NS get deploy"
ck_http "Le Service répond green" "$NS" "" "http://profile.$NS" "^green" "Le Service doit viser les Pods green." "kubectl -n $NS get endpointslices"
