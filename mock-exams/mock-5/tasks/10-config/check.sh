# Contrôles de m5-10 (sourcé après lib/check.sh)
ck_eq "LOG_LEVEL dans le conteneur" "warn" 'kn exec agent -- printenv LOG_LEVEL' "env.valueFrom.configMapKeyRef." "kubectl -n $NS get pod agent -o yaml | grep -A4 env"
ck_eq "API_TOKEN dans le conteneur" "s3cr3t-b2" 'kn exec agent -- printenv API_TOKEN' "env.valueFrom.secretKeyRef." "kubectl -n $NS get pod agent -o yaml | grep -A4 env"
ck_eq "API_TOKEN vient du Secret" "agent-sec" 'jp pod agent "{.spec.containers[0].env[?(@.name==\"API_TOKEN\")].valueFrom.secretKeyRef.name}"' "Pas de valeur en clair dans le Pod." "kubectl -n $NS get pod agent -o yaml | grep -A4 API_TOKEN"
