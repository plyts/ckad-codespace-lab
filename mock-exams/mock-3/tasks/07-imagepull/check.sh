# Contrôles de m3-07 (sourcé après lib/check.sh)
ck_true "Statut noté" "grep -qE 'ImagePullBackOff|ErrImagePull' $OUT/status.txt" "kubectl get pods : ErrImagePull puis ImagePullBackOff." "cat $OUT/status.txt"
ck_eq "Image corrigée, 2 prêts" "redis:7.4-alpine 2" 'jp deploy queue "{.spec.template.spec.containers[0].image} {.status.readyReplicas}"' "kubectl set image." "kubectl -n $NS describe pod -l app=queue | tail -5"
