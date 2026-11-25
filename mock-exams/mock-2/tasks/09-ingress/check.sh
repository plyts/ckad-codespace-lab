# Contrôles de m2-09 (sourcé après lib/check.sh)
ck_http "/ → home" "$NS" "" "--header=Host:m2.lab.local http://traefik.traefik.svc/" "^home" "Règle / vers home:80." "kubectl -n $NS describe ingress home-ing"
ck_http "/docs → docs" "$NS" "" "--header=Host:m2.lab.local http://traefik.traefik.svc/docs" "^docs" "Règle /docs vers docs:9090 (port du Service)." "kubectl -n $NS describe ingress home-ing"
ck_eq "Classe traefik" "traefik" 'jp ingress home-ing "{.spec.ingressClassName}"' "--class=traefik." "kubectl get ingressclass"
