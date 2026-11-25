# Contrôles de d4-06 (sourcé après lib/check.sh)
ck_eq "runAsUser / runAsGroup / fsGroup" "1000 3000 2000" 'jp pod secure "{.spec.securityContext.runAsUser} {.spec.securityContext.runAsGroup} {.spec.securityContext.fsGroup}"' \
  "Ces champs sont dans spec.securityContext (niveau Pod)." "kubectl -n $NS get pod secure -o yaml | grep -A4 securityContext"
ck_eq "allowPrivilegeEscalation false" "false" 'jp pod secure "{.spec.containers[0].securityContext.allowPrivilegeEscalation}"' \
  "Champ du conteneur : containers[].securityContext." "kubectl explain pod.spec.containers.securityContext"
ck_eq "readOnlyRootFilesystem true" "true" 'jp pod secure "{.spec.containers[0].securityContext.readOnlyRootFilesystem}"' \
  "Champ du conteneur uniquement (il n'existe pas au niveau Pod)." "kubectl explain pod.spec.containers.securityContext.readOnlyRootFilesystem"
ck_eq "capabilities drop ALL" "ALL" 'jp pod secure "{.spec.containers[0].securityContext.capabilities.drop[0]}"' \
  "capabilities: {drop: [ALL]} (au niveau conteneur)." "kubectl -n $NS get pod secure -o yaml | grep -A3 capabilities"
ck_eq "Le processus tourne en uid 1000" "1000" 'kn exec secure -- id -u' \
  "Le Pod doit tourner pour le vérifier." "kubectl -n $NS exec secure -- id"
ck_true "Écriture refusée sur /" "kubectl --context $CTX -n $NS exec secure -- true && ! kubectl --context $CTX -n $NS exec secure -- touch /test 2>/dev/null" \
  "Racine en lecture seule : touch /test doit échouer." "kubectl -n $NS exec secure -- touch /test"
