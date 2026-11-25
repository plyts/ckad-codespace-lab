# Contrôles de d1-05 (sourcé après lib/check.sh)
ck_eq "Init container prepare présent" "prepare" 'jp pod site "{.spec.initContainers[0].name}"' \
  "Un init container tourne jusqu'au bout AVANT les conteneurs principaux." "kubectl -n $NS get pod site -o yaml | grep -A3 initContainers"
ck_eq "Conteneur nginx présent" "nginx" 'jp pod site "{.spec.containers[0].name}"' \
  "Le conteneur principal doit s'appeler nginx." "kubectl -n $NS get pod site -o jsonpath='{.spec.containers[*].name}'"
ck_eq "Le Pod est prêt" "True" 'jp pod site "{.status.conditions[?(@.type==\"Ready\")].status}"' \
  "Si l'init container échoue, le Pod reste en Init:Error ou Init:CrashLoopBackOff." "kubectl -n $NS describe pod site | tail -20; kubectl -n $NS logs site -c prepare"
ck_http "HTTP sur le Pod renvoie « site prêt »" "$NS" "" "http://$(jp pod site '{.status.podIP}')/" "site prêt" \
  "nginx sert /usr/share/nginx/html : l'init doit écrire dans le même volume, sous le nom index.html." \
  "kubectl -n $NS exec site -c nginx -- cat /usr/share/nginx/html/index.html"
