# Contrôles de d4-01 (sourcé après lib/check.sh)
ck_eq "ConfigMap app-config" "prod blue" 'jp cm app-config "{.data.APP_MODE} {.data.APP_COLOR}"' \
  "kubectl create configmap app-config --from-literal=APP_MODE=prod --from-literal=APP_COLOR=blue" "kubectl -n $NS get cm app-config -o yaml"
ck_eq "Le Pod utilise envFrom" "app-config" 'jp pod app "{.spec.containers[0].envFrom[0].configMapRef.name}"' \
  "envFrom.configMapRef importe toutes les clés d'un coup (env.valueFrom : une clé à la fois)." "kubectl -n $NS get pod app -o yaml | grep -A3 envFrom"
ck_eq "Variables visibles dans le conteneur" "prod blue" 'echo $(kn exec app -- printenv APP_MODE) $(kn exec app -- printenv APP_COLOR)' \
  "Les variables ne sont lues qu'au démarrage du conteneur." "kubectl -n $NS exec app -- env | grep APP_"
