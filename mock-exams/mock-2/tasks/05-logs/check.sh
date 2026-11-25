# Contrôles de m2-05 (sourcé après lib/check.sh)
ck_eq "Ligne ERROR copiée" "ERROR BATCH=$(jp pod ingestor '{.spec.containers[0].env[0].value}')" 'head -1 $OUT/error.txt' \
  "kubectl logs ingestor | grep ERROR > fichier." "kubectl -n $NS logs ingestor | grep ERROR"
