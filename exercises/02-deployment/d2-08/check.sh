# Contrôles de d2-08 (sourcé après lib/check.sh)
ck_eq "api-v2 : 1 réplica prêt" "1" 'jp deploy api-v2 "{.status.readyReplicas}"' \
  "Un seul Pod canary sur 5 donne environ 20 % du trafic." "kubectl -n $NS get deploy -L track"
ck_eq "api-v1 réduit à 4 réplicas" "4" 'jp deploy api-v1 "{.spec.replicas}"' \
  "4 stables + 1 canary = 5 Pods : la proportion vient du nombre de Pods." "kubectl -n $NS get deploy"
ck_eq "Le canary porte app=api et track=canary" "api canary" 'jp deploy api-v2 "{.spec.template.metadata.labels.app} {.spec.template.metadata.labels.track}"' \
  "Le Service sélectionne app=api : le canary doit avoir ce label pour recevoir du trafic." "kubectl -n $NS get pods --show-labels"
ck_eq "5 Pods prêts derrière le Service" "5" 'kn get endpointslices -l kubernetes.io/service-name=api -o jsonpath="{range .items[*].endpoints[*]}{.conditions.ready}{\"\\n\"}{end}" | grep -c true' \
  "Le Service ne change pas : il voit tous les Pods app=api." "kubectl -n $NS get endpointslices -l kubernetes.io/service-name=api"
ck_true "Le sélecteur du Service n'a pas changé" "[ \"\$(jp svc api '{.spec.selector}')\" = '{\"app\":\"api\"}' ]" \
  "La consigne interdit de modifier le Service." "kubectl -n $NS get svc api -o jsonpath='{.spec.selector}'"
