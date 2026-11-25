# Contrôles de d2-05 (sourcé après lib/check.sh)
ck_eq "Stratégie RollingUpdate" "RollingUpdate" 'jp deploy api "{.spec.strategy.type}"' \
  "Deux stratégies : RollingUpdate (défaut) et Recreate." "kubectl -n $NS get deploy api -o yaml | grep -A4 strategy"
ck_eq "maxUnavailable = 0" "0" 'jp deploy api "{.spec.strategy.rollingUpdate.maxUnavailable}"' \
  "maxUnavailable: 0 garde la capacité pleine pendant la mise à jour." "kubectl explain deploy.spec.strategy.rollingUpdate"
ck_eq "maxSurge = 1" "1" 'jp deploy api "{.spec.strategy.rollingUpdate.maxSurge}"' \
  "maxSurge: 1 autorise un Pod de plus que replicas pendant la mise à jour." "kubectl -n $NS get deploy api -o yaml | grep -A4 strategy"
ck_eq "minReadySeconds = 5" "5" 'jp deploy api "{.spec.minReadySeconds}"' \
  "minReadySeconds est sous spec du Deployment, pas dans le template." "kubectl explain deploy.spec.minReadySeconds"
ck_eq "revisionHistoryLimit = 4" "4" 'jp deploy api "{.spec.revisionHistoryLimit}"' \
  "revisionHistoryLimit (10 par défaut) : nombre d'anciens ReplicaSets conservés." "kubectl explain deploy.spec.revisionHistoryLimit"
