# Contrôles de d3-06 (sourcé après lib/check.sh)
ck_eq "Raison notée" "FailedScheduling" 'tr -d "[:space:]" < $OUT/reason.txt' \
  "kubectl get events (ou describe pod) : colonne REASON. 50 CPU entiers ne tiennent sur aucun nœud." \
  "kubectl -n $NS get events --field-selector involvedObject.name=big"
ck_eq "Requête CPU 50m" "50m" 'jp pod big "{.spec.containers[0].resources.requests.cpu}"' \
  "50 = 50 cœurs ; 50m = 50 millicœurs. Les ressources d'un Pod se modifient en le recréant (ou par resize)." \
  "kubectl -n $NS get pod big -o yaml | grep -A3 resources"
ck_eq "Pod big Running" "Running" 'jp pod big "{.status.phase}"' \
  "Le Pod doit être ordonnancé puis démarrer." "kubectl -n $NS describe pod big | tail -8"
