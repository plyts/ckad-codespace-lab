# Contrôles de m1-03 (sourcé après lib/check.sh)
ck_eq "Readiness GET /index.html:80, 5 s" "/index.html 80 5" 'jp deploy catalog "{.spec.template.spec.containers[0].readinessProbe.httpGet.path} {.spec.template.spec.containers[0].readinessProbe.httpGet.port} {.spec.template.spec.containers[0].readinessProbe.periodSeconds}"' \
  "readinessProbe.httpGet + periodSeconds." "kubectl -n $NS get deploy catalog -o yaml | grep -A6 readiness"
ck_eq "Liveness TCP 80, 10 s / 15 s" "80 10 15" 'jp deploy catalog "{.spec.template.spec.containers[0].livenessProbe.tcpSocket.port} {.spec.template.spec.containers[0].livenessProbe.initialDelaySeconds} {.spec.template.spec.containers[0].livenessProbe.periodSeconds}"' \
  "livenessProbe.tcpSocket + initialDelaySeconds + periodSeconds." "kubectl -n $NS get deploy catalog -o yaml | grep -A6 liveness"
ck_eq "2 réplicas prêts et à jour" "2/2" 'echo "$(jp deploy catalog "{.status.updatedReplicas}")/$(jp deploy catalog "{.status.readyReplicas}")"' "/index.html doit exister dans nginx (/ marche)." "kubectl -n $NS get pods"
