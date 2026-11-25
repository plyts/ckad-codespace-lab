# Contrôles de d3-09 (sourcé après lib/check.sh)
ck_true "cause.txt mentionne la liveness" "grep -qi liveness $OUT/cause.txt" \
  "Les événements Unhealthy disent « Liveness probe failed … connection refused » : le port 8080 n'écoute pas." \
  "kubectl -n $NS get events | grep -i unhealthy | tail -3"
ck_eq "Liveness sur le port 5678" "5678" 'jp deploy orders "{.spec.template.spec.containers[0].livenessProbe.httpGet.port}"' \
  "http-echo écoute sur 5678 (voir containerPort)." "kubectl -n $NS get deploy orders -o yaml | grep -A5 livenessProbe"
ck_eq "Startup probe GET / 5678" "/ 5678" 'jp deploy orders "{.spec.template.spec.containers[0].startupProbe.httpGet.path} {.spec.template.spec.containers[0].startupProbe.httpGet.port}"' \
  "startupProbe : tant qu'elle n'a pas réussi, liveness et readiness sont suspendues." "kubectl explain deploy.spec.template.spec.containers.startupProbe"
ck_eq "Startup : failureThreshold 10, periodSeconds 2" "10 2" 'jp deploy orders "{.spec.template.spec.containers[0].startupProbe.failureThreshold} {.spec.template.spec.containers[0].startupProbe.periodSeconds}"' \
  "10 essais × 2 s = 20 s pour démarrer." "kubectl -n $NS get deploy orders -o yaml | grep -A6 startupProbe"
ck_eq "2 réplicas prêts et à jour" "2/2" 'echo "$(jp deploy orders "{.status.updatedReplicas}")/$(jp deploy orders "{.status.readyReplicas}")"' \
  "Après correction, le rolling update remplace les Pods." "kubectl -n $NS rollout status deploy/orders"
