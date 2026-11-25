# Contrôles de m4-14 (sourcé après lib/check.sh)
ck_http "/ → shop" "$NS" "" "--header=Host:m4.lab.local http://traefik.traefik.svc/" "^shop" "Règle / vers shop:80." "kubectl -n $NS describe ingress shop-ing"
ck_http "/cart → cart" "$NS" "" "--header=Host:m4.lab.local http://traefik.traefik.svc/cart" "^cart" "Règle /cart vers cart:9090 (port du Service)." "kubectl -n $NS describe ingress shop-ing"
ck_eq "Classe traefik" "traefik" 'jp ingress shop-ing "{.spec.ingressClassName}"' "--class=traefik." "kubectl get ingressclass"
