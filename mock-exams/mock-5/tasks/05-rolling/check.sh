# Contrôles de m5-05 (sourcé après lib/check.sh)
ck_eq "Image 1.28 et 4 réplicas prêts" "nginx:1.28-alpine 4" 'jp deploy portal "{.spec.template.spec.containers[0].image} {.status.readyReplicas}"' \
  "kubectl set image puis kubectl scale." "kubectl -n $NS get deploy portal -o wide"
ck_eq "Motif de la révision" "montée de version" 'jp deploy portal "{.metadata.annotations.kubernetes\.io/change-cause}"' \
  "kubectl annotate deploy portal kubernetes.io/change-cause='montée de version'." "kubectl -n $NS rollout history deploy/portal"
