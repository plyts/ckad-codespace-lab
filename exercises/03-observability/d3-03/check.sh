# Contrôles de d3-03 (sourcé après lib/check.sh)
ck_eq "Readiness tcpSocket 5678" "5678" 'jp deploy api "{.spec.template.spec.containers[0].readinessProbe.tcpSocket.port}"' \
  "readinessProbe.tcpSocket.port : la sonde ouvre une connexion TCP." "kubectl -n $NS get deploy api -o yaml | grep -A6 readiness"
ck_eq "periodSeconds 5 / initialDelaySeconds 2" "5 2" 'jp deploy api "{.spec.template.spec.containers[0].readinessProbe.periodSeconds} {.spec.template.spec.containers[0].readinessProbe.initialDelaySeconds}"' \
  "Les deux délais sont dans la sonde." "kubectl -n $NS get deploy api -o yaml | grep -A6 readiness"
ck_eq "2 réplicas prêts" "2" 'jp deploy api "{.status.readyReplicas}"' \
  "Readiness : un Pod non prêt est retiré des Endpoints du Service, sans redémarrage." "kubectl -n $NS get pods"
