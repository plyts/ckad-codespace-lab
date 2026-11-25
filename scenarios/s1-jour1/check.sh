# Contrôles de s1-jour1 (sourcé après lib/check.sh)
for d in redis:1 api:2 front:2; do
  n=${d%%:*}; r=${d##*:}
  ck_eq "Deployment $n : $r réplica(s) prêt(s)" "$r" "jp deploy $n '{.status.readyReplicas}'" \
    "Crée le Deployment $n avec $r réplica(s) et attends qu'il soit prêt." "kubectl -n $NS get deploy,pods -l app=$n"
done
ck_eq "Service redis 6379" "6379" 'jp svc redis "{.spec.ports[0].port}"' \
  "kubectl expose deploy redis --port=6379." "kubectl -n $NS get svc"
ck_eq "Service api : 80 → 5678" "80 5678" 'jp svc api "{.spec.ports[0].port} {.spec.ports[0].targetPort}"' \
  "Le Service publie le port 80, le conteneur écoute sur 5678." "kubectl -n $NS describe svc api"
ck_http "http://api répond « api v1 »" "$NS" "" "http://api.$NS" "api v1" \
  "Sélecteur et ports du Service api." "kubectl -n $NS get endpointslices"
ck_http "http://front répond (nginx)" "$NS" "" "http://front.$NS" "Welcome to nginx" \
  "Service front, port 80." "kubectl -n $NS get svc front"
