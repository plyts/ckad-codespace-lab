# Contrôles de m4-06 (sourcé après lib/check.sh)
ck_eq "Canary : 1 prêt(s)" "1" 'jp deploy pricing-canary "{.status.readyReplicas}"' "Le canary porte app=pricing." "kubectl -n $NS get deploy -L track"
ck_eq "Stable réduit à 4" "4" 'jp deploy pricing-stable "{.spec.replicas}"' "4 + 1 = 5." "kubectl -n $NS get deploy"
ck_eq "5 Endpoints prêts" "5" 'kn get endpointslices -l kubernetes.io/service-name=pricing -o jsonpath="{range .items[*].endpoints[*]}{.conditions.ready}{\" \"}{end}" | grep -o true | wc -l | tr -d " "' \
  "Le Service voit tous les Pods app=pricing." "kubectl -n $NS get endpointslices"
