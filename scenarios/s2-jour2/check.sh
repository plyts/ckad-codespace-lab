# Contrôles de s2-jour2 (sourcé après lib/check.sh)
ck_http "front sert « Boutique jour 2 »" "$NS" "" "http://front.$NS" "Boutique jour 2" \
  "Volume configMap front-html monté sur /usr/share/nginx/html du conteneur front." "kubectl -n $NS exec deploy/front -- cat /usr/share/nginx/html/index.html"
ck_eq "REDIS_PASSWORD depuis redis-auth" "redis-auth/password" 'jp deploy api "{.spec.template.spec.containers[0].env[?(@.name==\"REDIS_PASSWORD\")].valueFrom.secretKeyRef.name}/{.spec.template.spec.containers[0].env[?(@.name==\"REDIS_PASSWORD\")].valueFrom.secretKeyRef.key}"' \
  "env.valueFrom.secretKeyRef dans le conteneur api." "kubectl -n $NS get deploy api -o yaml | grep -A4 env"
ck_eq "Secret : password" "r3d1s-pass" 'jp secret redis-auth "{.data.password}" | base64 -d' \
  "kubectl create secret generic redis-auth --from-literal=password=r3d1s-pass." "kubectl -n $NS get secret redis-auth -o yaml"
ck_eq "Ressources de api" "50m 32Mi 100m 64Mi" 'jp deploy api "{.spec.template.spec.containers[0].resources.requests.cpu} {.spec.template.spec.containers[0].resources.requests.memory} {.spec.template.spec.containers[0].resources.limits.cpu} {.spec.template.spec.containers[0].resources.limits.memory}"' \
  "kubectl set resources deploy api --requests=cpu=50m,memory=32Mi --limits=cpu=100m,memory=64Mi." "kubectl -n $NS get deploy api -o yaml | grep -A6 resources"
ck_eq "api : 3 réplicas prêts et à jour" "3/3" 'echo "$(jp deploy api "{.status.updatedReplicas}")/$(jp deploy api "{.status.readyReplicas}")"' \
  "kubectl scale deploy api --replicas=3." "kubectl -n $NS get deploy api"
