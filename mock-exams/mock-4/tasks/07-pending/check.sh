# Contrôles de m4-07 (sourcé après lib/check.sh)
ck_eq "Pod Running" "Running" 'jp pod batch "{.status.phase}"' \
  "FailedScheduling : aucun nœud n'a le label disk=ssd demandé par nodeSelector. Recrée le Pod sans ce nodeSelector." "kubectl -n $NS describe pod batch | tail -5"
ck_true "Nœuds non modifiés (aucun label disk)" "! kubectl --context $CTX get nodes -l disk -o name | grep -q ." "La consigne interdit d'étiqueter les nœuds." "kubectl get nodes --show-labels"
