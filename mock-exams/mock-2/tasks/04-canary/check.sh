# Contrôles de m2-04 (sourcé après lib/check.sh)
ck_eq "Canary : 1 prêt(s)" "1" 'jp deploy search-canary "{.status.readyReplicas}"' "Le canary porte app=search." "kubectl -n $NS get deploy -L track"
ck_eq "Stable réduit à 3" "3" 'jp deploy search-stable "{.spec.replicas}"' "3 + 1 = 4." "kubectl -n $NS get deploy"
ck_eq "4 Endpoints prêts" "4" 'kn get endpointslices -l kubernetes.io/service-name=search -o jsonpath="{range .items[*].endpoints[*]}{.conditions.ready}{\" \"}{end}" | grep -o true | wc -l | tr -d " "' \
  "Le Service voit tous les Pods app=search." "kubectl -n $NS get endpointslices"
