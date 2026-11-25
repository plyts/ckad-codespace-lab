# Contrôles de m3-10 (sourcé après lib/check.sh)
ck_eq "Ressources" "100m 128Mi 100m 128Mi" 'jp deploy api "{.spec.template.spec.containers[0].resources.requests.cpu} {.spec.template.spec.containers[0].resources.requests.memory} {.spec.template.spec.containers[0].resources.limits.cpu} {.spec.template.spec.containers[0].resources.limits.memory}"' \
  "kubectl set resources deploy api --requests=… --limits=…" "kubectl -n $NS get deploy api -o yaml | grep -A6 resources"
ck_eq "QoS notée" "Guaranteed" 'tr -d "[:space:]" < $OUT/qos.txt' "requests = limits : Guaranteed ; sinon Burstable." "kubectl -n $NS get pod -l app=api -o jsonpath='{.items[0].status.qosClass}'"
