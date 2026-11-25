# Contrôles de s3-jour3 (sourcé après lib/check.sh)
ck_true "incident.txt : statut noté" "grep -qE 'CrashLoopBackOff|Error' $OUT/incident.txt" \
  "kubectl get pods montre Error puis CrashLoopBackOff (le kubelet espace les redémarrages)." "kubectl -n $NS get pods -l app=api"
ck_true "incident.txt : cause notée" "grep -qiE 'flag provided but not defined|-timeout' $OUT/incident.txt" \
  "kubectl logs <pod> (ou --previous) affiche : flag provided but not defined: -timeout (option inconnue de la v2)." "kubectl -n $NS logs -l app=api --tail=3"
ck_eq "Révision v1 restaurée" "-text=api v1" 'jp deploy api "{.spec.template.spec.containers[0].args[*]}"' \
  "kubectl rollout undo deploy/api (ou --to-revision=N, voir rollout history)." "kubectl -n $NS rollout history deploy/api"
ck_eq "3 réplicas prêts et à jour" "3/3" 'echo "$(jp deploy api "{.status.updatedReplicas}")/$(jp deploy api "{.status.readyReplicas}")"' \
  "Après le rollback, plus aucun Pod v2." "kubectl -n $NS get pods -l app=api"
ck_http "L'API répond api v1" "$NS" "" "http://api.$NS" "api v1" \
  "Le Service api renvoie vers les Pods v1." "kubectl -n $NS get endpointslices -l kubernetes.io/service-name=api"
