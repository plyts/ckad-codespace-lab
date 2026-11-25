# Contrôles de m4-09 (sourcé après lib/check.sh)
ck_eq "Readiness GET /:80, 5 s" "/ 80 5" 'jp deploy media "{.spec.template.spec.containers[0].readinessProbe.httpGet.path} {.spec.template.spec.containers[0].readinessProbe.httpGet.port} {.spec.template.spec.containers[0].readinessProbe.periodSeconds}"' \
  "readinessProbe.httpGet + periodSeconds." "kubectl -n $NS get deploy media -o yaml | grep -A6 readiness"
ck_eq "Liveness TCP 80, 10 s / 15 s" "80 10 15" 'jp deploy media "{.spec.template.spec.containers[0].livenessProbe.tcpSocket.port} {.spec.template.spec.containers[0].livenessProbe.initialDelaySeconds} {.spec.template.spec.containers[0].livenessProbe.periodSeconds}"' \
  "livenessProbe.tcpSocket + initialDelaySeconds + periodSeconds." "kubectl -n $NS get deploy media -o yaml | grep -A6 liveness"
ck_eq "2 réplicas prêts et à jour" "2/2" 'echo "$(jp deploy media "{.status.updatedReplicas}")/$(jp deploy media "{.status.readyReplicas}")"' "/ doit exister dans nginx (/ marche)." "kubectl -n $NS get pods"
