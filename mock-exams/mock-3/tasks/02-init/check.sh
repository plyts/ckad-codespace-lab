# Contrôles de m3-02 (sourcé après lib/check.sh)
ck_eq "Init container seed" "seed" 'jp pod landing "{.spec.initContainers[0].name}"' "initContainers[0].name = seed." "kubectl -n $NS get pod landing -o yaml | grep -A3 initContainers"
ck_eq "Pod prêt" "True" 'jp pod landing "{.status.conditions[?(@.type==\"Ready\")].status}"' "Le Pod doit tourner." "kubectl -n $NS describe pod landing | tail"
ck_http "Le Pod sert « bienvenue m3 »" "$NS" "" "http://$(jp pod landing '{.status.podIP}')/" "bienvenue m3" \
  "L'init écrit dans le volume que nginx sert." "kubectl -n $NS exec landing -c web -- cat /usr/share/nginx/html/index.html"
