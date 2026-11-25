# Contrôles de m5-08 (sourcé après lib/check.sh)
ck_true "Statut noté" "grep -qE 'ImagePullBackOff|ErrImagePull' $OUT/status.txt" "kubectl get pods : ErrImagePull puis ImagePullBackOff." "cat $OUT/status.txt"
ck_eq "Image corrigée, 2 prêts" "nginx:1.27-alpine 2" 'jp deploy frontend "{.spec.template.spec.containers[0].image} {.status.readyReplicas}"' "kubectl set image." "kubectl -n $NS describe pod -l app=frontend | tail -5"
