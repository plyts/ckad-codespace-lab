# Contrôles de d4-04 (sourcé après lib/check.sh)
ck_eq "Requests 100m / 64Mi" "100m 64Mi" 'jp pod bounded "{.spec.containers[0].resources.requests.cpu} {.spec.containers[0].resources.requests.memory}"' \
  "resources.requests : ce que le scheduler réserve." "kubectl -n $NS get pod bounded -o yaml | grep -A6 resources"
ck_eq "Limits 200m / 128Mi" "200m 128Mi" 'jp pod bounded "{.spec.containers[0].resources.limits.cpu} {.spec.containers[0].resources.limits.memory}"' \
  "resources.limits : au-delà, CPU bridé et mémoire tuée (OOMKilled)." "kubectl -n $NS get pod bounded -o yaml | grep -A6 resources"
ck_eq "Classe QoS notée" "Burstable" 'tr -d "[:space:]" < $OUT/qos.txt' \
  "requests < limits : Burstable. requests = limits partout : Guaranteed. Rien : BestEffort." "kubectl -n $NS get pod bounded -o jsonpath='{.status.qosClass}'"
ck_eq "Pod prêt" "true" 'jp pod bounded "{.status.containerStatuses[0].ready}"' \
  "Le Pod doit tourner." "kubectl -n $NS describe pod bounded | tail"
