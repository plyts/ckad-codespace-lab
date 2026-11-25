# Contrôles de m3-04 (sourcé après lib/check.sh)
ck_eq "stg-shop : 2 prêts, image 1.28" "2 nginx:1.28-alpine" 'jp deploy stg-shop "{.status.readyReplicas} {.spec.template.spec.containers[0].image}"' \
  "namePrefix, replicas et images dans le kustomization.yaml de l'overlay." "kubectl kustomize ~/ckad/m3-04/overlay"
ck_eq "Label tier=staging" "staging" 'jp deploy stg-shop "{.metadata.labels.tier}"' "labels: - pairs: {tier: staging}." "kubectl -n $NS get deploy --show-labels"
