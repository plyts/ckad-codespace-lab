# Contrôles de d5-05 (sourcé après lib/check.sh)
ck_eq "ingressClassName traefik" "traefik" 'jp ingress shop "{.spec.ingressClassName}"' \
  "Le contrôleur du labo est Traefik (classe traefik). À l'examen, la classe est donnée dans la consigne." "kubectl get ingressclass"
ck_eq "Hôte shop.lab.local" "shop.lab.local" 'jp ingress shop "{.spec.rules[0].host}"' \
  "rules[].host." "kubectl -n $NS describe ingress shop"
ck_http "/ → front" "$NS" "" "--header=Host:shop.lab.local http://traefik.traefik.svc/" "^front" \
  "La règle / (Prefix) doit viser le Service front, port 80." "kubectl -n $NS describe ingress shop"
ck_http "/api → api" "$NS" "" "--header=Host:shop.lab.local http://traefik.traefik.svc/api/v1" "^api" \
  "La règle /api (Prefix) doit viser le Service api, port 8080 (le port du Service, pas celui du conteneur)." "kubectl -n $NS describe ingress shop"
