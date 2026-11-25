# Contrôles de d5-03 (sourcé après lib/check.sh)
ck_eq "FQDN" "db.$NS.svc.cluster.local" 'tr -d "[:space:]" < $OUT/fqdn.txt' \
  "Forme : <service>.<namespace>.svc.cluster.local (cluster.local est le domaine par défaut)." "kubectl -n $NS get svc db"
ck_eq "ClusterIP" "$(jp svc db '{.spec.clusterIP}')" 'tr -d "[:space:]" < $OUT/ip.txt' \
  "kubectl get svc db -o jsonpath='{.spec.clusterIP}'." "kubectl -n $NS get svc db -o wide"
