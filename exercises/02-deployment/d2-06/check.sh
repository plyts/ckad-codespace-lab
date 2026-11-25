# Contrôles de d2-06 (sourcé après lib/check.sh)
ck_match "Release shop déployée" "(^|[[:space:]])shop([[:space:]]|$)" 'helm --kube-context "$CTX" -n "$NS" list -q --deployed' \
  "helm install <release> <chart> -n <namespace>." "helm -n $NS list -a"
ck_eq "replicaCount = 2" "2" 'jp deploy shop-webapp "{.spec.replicas}"' \
  "Les valeurs se passent avec --set replicaCount=2 (ou -f values.yaml)." "helm -n $NS get values shop"
ck_eq "Image nginx:1.28-alpine" "nginx:1.28-alpine" 'jp deploy shop-webapp "{.spec.template.spec.containers[0].image}"' \
  "--set image.tag=1.28-alpine : la clé imbriquée s'écrit avec un point." "helm -n $NS get values shop"
ck_eq "2 réplicas prêts" "2" 'jp deploy shop-webapp "{.status.readyReplicas}"' \
  "Les Pods de la release doivent tourner." "kubectl -n $NS get pods"
ck_true "values.txt contient les valeurs par défaut" "grep -q 'replicaCount: 1' $OUT/values.txt && grep -q 'tag: 1.27-alpine' $OUT/values.txt" \
  "helm show values <chart> > fichier." "cat $OUT/values.txt"
