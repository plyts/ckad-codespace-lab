# Contrôles de m4-08 (sourcé après lib/check.sh)
ck_eq "Ligne ERROR copiée" "ERROR SYNC=$(jp pod sync '{.spec.containers[0].env[0].value}')" 'head -1 $OUT/error.txt' \
  "kubectl logs sync | grep ERROR > fichier." "kubectl -n $NS logs sync | grep ERROR"
