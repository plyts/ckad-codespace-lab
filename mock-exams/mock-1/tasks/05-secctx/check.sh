# Contrôles de m1-05 (sourcé après lib/check.sh)
ck_eq "uid 2000 et runAsNonRoot" "2000 true" 'jp pod hardened "{.spec.securityContext.runAsUser}{.spec.containers[0].securityContext.runAsUser} {.spec.securityContext.runAsNonRoot}{.spec.containers[0].securityContext.runAsNonRoot}"' \
  "runAsUser et runAsNonRoot (niveau Pod ou conteneur)." "kubectl -n $NS get pod hardened -o yaml | grep -A6 -i securityContext"
ck_eq "drop ALL, add NET_BIND_SERVICE" "ALL NET_BIND_SERVICE" 'jp pod hardened "{.spec.containers[0].securityContext.capabilities.drop[0]} {.spec.containers[0].securityContext.capabilities.add[0]}"' \
  "capabilities: {drop: [ALL], add: [NET_BIND_SERVICE]} (niveau conteneur seulement)." "kubectl explain pod.spec.containers.securityContext.capabilities"
ck_eq "Pas d'escalade" "false" 'jp pod hardened "{.spec.containers[0].securityContext.allowPrivilegeEscalation}"' "allowPrivilegeEscalation: false." "kubectl -n $NS get pod hardened -o yaml | grep -i escalation"
ck_eq "id -u = 2000" "2000" 'kn exec hardened -- id -u' "Le Pod doit tourner." "kubectl -n $NS describe pod hardened | tail"
