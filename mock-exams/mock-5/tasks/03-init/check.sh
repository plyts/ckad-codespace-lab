# Contrôles de m5-03 (sourcé après lib/check.sh)
ck_eq "Init container seed" "seed" 'jp pod status "{.spec.initContainers[0].name}"' "initContainers[0].name = seed." "kubectl -n $NS get pod status -o yaml | grep -A3 initContainers"
ck_eq "Pod prêt" "True" 'jp pod status "{.status.conditions[?(@.type==\"Ready\")].status}"' "Le Pod doit tourner." "kubectl -n $NS describe pod status | tail"
ck_http "Le Pod sert « tout va bien »" "$NS" "" "http://$(jp pod status '{.status.podIP}')/" "tout va bien" \
  "L'init écrit dans le volume que nginx sert." "kubectl -n $NS exec status -c web -- cat /usr/share/nginx/html/index.html"
