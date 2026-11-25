# Contrôles de m3-06 (sourcé après lib/check.sh)
ck_eq "Stratégie Recreate" "Recreate" 'jp deploy legacy "{.spec.strategy.type}"' \
  "Recreate : retirer aussi strategy.rollingUpdate, sinon l'API refuse." "kubectl -n $NS get deploy legacy -o yaml | grep -A3 strategy"
ck_eq "Image 1.28, 2 prêts" "nginx:1.28-alpine 2" 'jp deploy legacy "{.spec.template.spec.containers[0].image} {.status.readyReplicas}"' "kubectl set image." "kubectl -n $NS rollout status deploy/legacy"
