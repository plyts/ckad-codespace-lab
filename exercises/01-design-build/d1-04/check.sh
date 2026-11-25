# Contrôles de d1-04 (sourcé après lib/check.sh)
ck_eq "Le Pod logger est Running" "Running" 'jp pod logger "{.status.phase}"' \
  "Le Pod doit tourner avec ses deux conteneurs." "kubectl -n $NS describe pod logger | tail -20"
ck_match "Conteneur app présent" "(^| )app( |$)" 'jp pod logger "{.spec.containers[*].name}"' \
  "Le conteneur principal doit s'appeler app." "kubectl -n $NS get pod logger -o jsonpath='{.spec.containers[*].name}'"
ck_match "Conteneur shipper présent" "(^| )shipper( |$)" 'jp pod logger "{.spec.containers[*].name} {.spec.initContainers[*].name}"' \
  "Le sidecar doit s'appeler shipper." "kubectl -n $NS get pod logger -o yaml | grep 'name:'"
ck_eq "shipper est un sidecar natif (initContainer, restartPolicy Always)" "Always" \
  'jp pod logger "{.spec.initContainers[?(@.name==\"shipper\")].restartPolicy}"' \
  "Depuis Kubernetes 1.29, un sidecar natif est un initContainer avec restartPolicy: Always : il démarre avant app et vit avec le Pod." \
  "kubectl explain pod.spec.initContainers.restartPolicy"
ck_eq "Les deux conteneurs montent /var/log/app" "/var/log/app /var/log/app" \
  'jp pod logger "{.spec.containers[?(@.name==\"app\")].volumeMounts[0].mountPath} {.spec.initContainers[?(@.name==\"shipper\")].volumeMounts[0].mountPath}"' \
  "Le partage passe par un même volume monté dans les deux conteneurs." "kubectl -n $NS get pod logger -o yaml | grep -B2 -A3 volumeMounts"
ck_true "kubectl logs logger -c shipper montre des lignes tick" "kubectl --context $CTX -n $NS logs logger -c shipper --tail=5 | grep -q tick" \
  "Le sidecar lit le fichier écrit par app : vérifie le volume et le chemin app.log." "kubectl -n $NS logs logger -c shipper --tail=5"
