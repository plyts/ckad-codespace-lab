# Contrôles de d5-08 (sourcé après lib/check.sh)
ck_eq "Classe existante (traefik)" "traefik" 'jp ingress blog "{.spec.ingressClassName}"' \
  "Aucune IngressClass nginx dans ce cluster : aucun contrôleur ne prend l'Ingress (pas d'ADDRESS)." "kubectl get ingressclass; kubectl -n $NS get ingress"
ck_eq "Port du Service : 80" "80" 'jp ingress blog "{.spec.rules[0].http.paths[0].backend.service.port.number}"' \
  "Le backend vise le port du SERVICE (80), pas 8080." "kubectl -n $NS get svc blog"
ck_http "blog.lab.local renvoie « blog ok »" "$NS" "" "--header=Host:blog.lab.local http://traefik.traefik.svc/" "blog ok" \
  "Classe + port justes : Traefik route la requête." "kubectl -n $NS describe ingress blog"
