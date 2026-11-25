# Contrôles de m1-02 (sourcé après lib/check.sh)
ck_eq "Image 1.28 et 4 réplicas prêts" "nginx:1.28-alpine 4" 'jp deploy storefront "{.spec.template.spec.containers[0].image} {.status.readyReplicas}"' \
  "kubectl set image puis kubectl scale." "kubectl -n $NS get deploy storefront -o wide"
ck_eq "Motif de la révision" "nginx 1.28" 'jp deploy storefront "{.metadata.annotations.kubernetes\.io/change-cause}"' \
  "kubectl annotate deploy storefront kubernetes.io/change-cause='nginx 1.28'." "kubectl -n $NS rollout history deploy/storefront"
