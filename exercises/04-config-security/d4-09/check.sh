# Contrôles de d4-09 (sourcé après lib/check.sh)
ck_eq "2 réplicas prêts" "2" 'jp deploy portal "{.status.readyReplicas}"' \
  "Le Deployment doit tourner." "kubectl -n $NS get deploy,pods"
ck_eq "ServiceAccount portal-sa" "portal-sa" 'jp deploy portal "{.spec.template.spec.serviceAccountName}"' \
  "spec.template.spec.serviceAccountName." "kubectl -n $NS get deploy portal -o yaml | grep serviceAccount"
ck_eq "Requests 50m / 32Mi" "50m 32Mi" 'jp deploy portal "{.spec.template.spec.containers[0].resources.requests.cpu} {.spec.template.spec.containers[0].resources.requests.memory}"' \
  "resources.requests du conteneur." "kubectl -n $NS get deploy portal -o yaml | grep -A4 resources"
ck_eq "API_KEY lue dans le Secret" "k-7731" 'kn exec deploy/portal -- printenv API_KEY' \
  "env.valueFrom.secretKeyRef {name: portal-key, key: API_KEY}." "kubectl -n $NS exec deploy/portal -- env | grep API"
ck_http "nginx sert « Portal OK »" "$NS" "" "http://$(kn get pod -l app=portal -o jsonpath='{.items[0].status.podIP}')/" "Portal OK" \
  "Le volume configMap crée un fichier par clé : index.html dans /usr/share/nginx/html." "kubectl -n $NS exec deploy/portal -- ls /usr/share/nginx/html"
