# Contrôles de d2-02 (sourcé après lib/check.sh)
ck_eq "replicas = 5" "5" 'jp deploy front "{.spec.replicas}"' \
  "kubectl scale modifie spec.replicas du Deployment." "kubectl -n $NS get deploy front"
ck_eq "5 réplicas prêts" "5" 'jp deploy front "{.status.readyReplicas}"' \
  "Les nouveaux Pods doivent démarrer." "kubectl -n $NS get pods -l app=front"
ck_true "Deployment non recréé (même UID qu'au départ)" "[ \"\$(jp deploy front '{.metadata.annotations.deployment\.kubernetes\.io/revision}')\" = 1 ]" \
  "Mettre à l'échelle ne crée pas de nouvelle révision : seul le nombre de Pods change." "kubectl -n $NS rollout history deploy/front"
