# Contrôles de m5-09 (sourcé après lib/check.sh)
ck_eq "Fichier en networking.k8s.io/v1" "1" 'grep -c "apiVersion: networking.k8s.io/v1$" $OUT/ingress.yaml' \
  "v1beta1 retiré en 1.22. En v1 : pathType obligatoire, backend.service.name et backend.service.port.number." "kubectl explain ingress.spec.rules.http.paths.backend"
ck_http "old.m5.lab.local répond « web ok »" "$NS" "" "--header=Host:old.m5.lab.local http://traefik.traefik.svc/" "web ok" "L'Ingress converti doit être appliqué." "kubectl -n $NS describe ingress old-site"
