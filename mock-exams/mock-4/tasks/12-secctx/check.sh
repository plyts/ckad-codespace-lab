# Contrôles de m4-12 (sourcé après lib/check.sh)
ck_eq "uid 1500 et runAsNonRoot" "1500 true" 'jp pod runner "{.spec.securityContext.runAsUser}{.spec.containers[0].securityContext.runAsUser} {.spec.securityContext.runAsNonRoot}{.spec.containers[0].securityContext.runAsNonRoot}"' \
  "runAsUser et runAsNonRoot (niveau Pod ou conteneur)." "kubectl -n $NS get pod runner -o yaml | grep -A6 -i securityContext"
ck_eq "drop ALL, add NET_BIND_SERVICE" "ALL NET_BIND_SERVICE" 'jp pod runner "{.spec.containers[0].securityContext.capabilities.drop[0]} {.spec.containers[0].securityContext.capabilities.add[0]}"' \
  "capabilities: {drop: [ALL], add: [NET_BIND_SERVICE]} (niveau conteneur seulement)." "kubectl explain pod.spec.containers.securityContext.capabilities"
ck_eq "Pas d'escalade" "false" 'jp pod runner "{.spec.containers[0].securityContext.allowPrivilegeEscalation}"' "allowPrivilegeEscalation: false." "kubectl -n $NS get pod runner -o yaml | grep -i escalation"
ck_eq "id -u = 1500" "1500" 'kn exec runner -- id -u' "Le Pod doit tourner." "kubectl -n $NS describe pod runner | tail"
