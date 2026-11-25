# Contrôles de d3-02 (sourcé après lib/check.sh)
ck_eq "Liveness httpGet sur /" "/" 'jp pod web "{.spec.containers[0].livenessProbe.httpGet.path}"' \
  "livenessProbe.httpGet.path : / ." "kubectl -n $NS get pod web -o yaml | grep -A8 livenessProbe"
ck_eq "Port 80" "80" 'jp pod web "{.spec.containers[0].livenessProbe.httpGet.port}"' \
  "livenessProbe.httpGet.port : 80." "kubectl explain pod.spec.containers.livenessProbe.httpGet"
ck_eq "initialDelaySeconds = 5" "5" 'jp pod web "{.spec.containers[0].livenessProbe.initialDelaySeconds}"' \
  "Délai avant le premier essai." "kubectl explain pod.spec.containers.livenessProbe.initialDelaySeconds"
ck_eq "periodSeconds = 10" "10" 'jp pod web "{.spec.containers[0].livenessProbe.periodSeconds}"' \
  "Intervalle entre deux essais." "kubectl explain pod.spec.containers.livenessProbe.periodSeconds"
ck_eq "Pod prêt, sans redémarrage" "true 0" 'jp pod web "{.status.containerStatuses[0].ready} {.status.containerStatuses[0].restartCount}"' \
  "Une liveness qui échoue redémarre le conteneur." "kubectl -n $NS describe pod web | grep -A5 -i liveness"
