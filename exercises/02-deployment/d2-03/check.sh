# Contrôles de d2-03 (sourcé après lib/check.sh)
ck_eq "Image nginx:1.28-alpine" "nginx:1.28-alpine" 'jp deploy front "{.spec.template.spec.containers[0].image}"' \
  "kubectl set image deploy/front nginx=nginx:1.28-alpine (nom du conteneur = nginx)." "kubectl -n $NS get deploy front -o wide"
ck_eq "Révision 2" "2" 'jp deploy front "{.metadata.annotations.deployment\.kubernetes\.io/revision}"' \
  "Chaque changement du template crée une révision (un nouveau ReplicaSet)." "kubectl -n $NS rollout history deploy/front"
ck_eq "Motif dans l'historique" "passage en 1.28" 'jp deploy front "{.metadata.annotations.kubernetes\.io/change-cause}"' \
  "--record est supprimé : on annote le Deployment après la mise à jour." "kubectl -n $NS rollout history deploy/front"
ck_eq "Tous les réplicas à jour et prêts" "3/3" 'echo "$(jp deploy front "{.status.updatedReplicas}")/$(jp deploy front "{.status.readyReplicas}")"' \
  "Le rolling update doit être terminé." "kubectl -n $NS rollout status deploy/front"
