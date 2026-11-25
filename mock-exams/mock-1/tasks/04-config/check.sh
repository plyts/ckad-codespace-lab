# Contrôles de m1-04 (sourcé après lib/check.sh)
ck_eq "LOG_LEVEL dans le conteneur" "debug" 'kn exec worker -- printenv LOG_LEVEL' "env.valueFrom.configMapKeyRef." "kubectl -n $NS get pod worker -o yaml | grep -A4 env"
ck_eq "API_TOKEN dans le conteneur" "t0k3n-a1" 'kn exec worker -- printenv API_TOKEN' "env.valueFrom.secretKeyRef." "kubectl -n $NS get pod worker -o yaml | grep -A4 env"
ck_eq "API_TOKEN vient du Secret" "worker-sec" 'jp pod worker "{.spec.containers[0].env[?(@.name==\"API_TOKEN\")].valueFrom.secretKeyRef.name}"' "Pas de valeur en clair dans le Pod." "kubectl -n $NS get pod worker -o yaml | grep -A4 API_TOKEN"
