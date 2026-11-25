# Contrôles de m4-04 (sourcé après lib/check.sh)
ck_eq "Image revenue à redis:7.4-alpine, 2 réplicas prêts" "redis:7.4-alpine 2" 'jp deploy sessions "{.spec.template.spec.containers[0].image} {.status.readyReplicas}"' \
  "kubectl rollout undo deploy/sessions." "kubectl -n $NS rollout history deploy/sessions"
ck_eq "Révision notée" "1" 'tr -d "[:space:]" < $OUT/revision.txt' "rollout history : la révision qui marchait est la 1." "kubectl -n $NS rollout history deploy/sessions"
