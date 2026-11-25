# Contrôles de m5-11 (sourcé après lib/check.sh)
ck_eq "Ressources" "200m 256Mi 500m 512Mi" 'jp deploy render "{.spec.template.spec.containers[0].resources.requests.cpu} {.spec.template.spec.containers[0].resources.requests.memory} {.spec.template.spec.containers[0].resources.limits.cpu} {.spec.template.spec.containers[0].resources.limits.memory}"' \
  "kubectl set resources deploy render --requests=… --limits=…" "kubectl -n $NS get deploy render -o yaml | grep -A6 resources"
ck_eq "QoS notée" "Burstable" 'tr -d "[:space:]" < $OUT/qos.txt' "requests = limits : Guaranteed ; sinon Burstable." "kubectl -n $NS get pod -l app=render -o jsonpath='{.items[0].status.qosClass}'"
