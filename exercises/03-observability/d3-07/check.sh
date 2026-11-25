# Contrôles de d3-07 (sourcé après lib/check.sh)
ck_eq "CronJob cleanup créé" "cleanup" 'jp cronjob cleanup "{.metadata.name}"' \
  "batch/v1beta1 CronJob a été retiré en 1.25 : utiliser batch/v1." "kubectl api-resources | grep -i cronjob"
ck_eq "PDB web-pdb créé" "web-pdb" 'jp pdb web-pdb "{.metadata.name}"' \
  "policy/v1beta1 PodDisruptionBudget a été retiré en 1.25 : utiliser policy/v1." "kubectl explain pdb | head -3"
ck_eq "Plus aucune API v1beta1 dans le fichier" "0" 'grep -c "v1beta1" $OUT/old.yaml' \
  "La consigne demande de corriger le fichier (il sera réutilisé)." "grep -n apiVersion $OUT/old.yaml"
