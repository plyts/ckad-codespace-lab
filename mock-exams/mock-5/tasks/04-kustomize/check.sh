# Contrôles de m5-04 (sourcé après lib/check.sh)
ck_eq "prd-shop : 3 prêts, image 1.28" "3 nginx:1.28-alpine" 'jp deploy prd-shop "{.status.readyReplicas} {.spec.template.spec.containers[0].image}"' \
  "namePrefix, replicas et images dans le kustomization.yaml de l'overlay." "kubectl kustomize ~/ckad/m5-04/overlay"
ck_eq "Label tier=prod" "prod" 'jp deploy prd-shop "{.metadata.labels.tier}"' "labels: - pairs: {tier: prod}." "kubectl -n $NS get deploy --show-labels"
