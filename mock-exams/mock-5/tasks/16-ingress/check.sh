# Contrôles de m5-16 (sourcé après lib/check.sh)
ck_http "/ → front" "$NS" "" "--header=Host:m5.lab.local http://traefik.traefik.svc/" "^front" "Règle / vers front:80." "kubectl -n $NS describe ingress front-ing"
ck_http "/api → api" "$NS" "" "--header=Host:m5.lab.local http://traefik.traefik.svc/api" "^api" "Règle /api vers api:9090 (port du Service)." "kubectl -n $NS describe ingress front-ing"
ck_eq "Classe traefik" "traefik" 'jp ingress front-ing "{.spec.ingressClassName}"' "--class=traefik." "kubectl get ingressclass"
