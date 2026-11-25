# Contrôles de d2-04 (sourcé après lib/check.sh)
ck_eq "Image revenue à nginx:1.27-alpine" "nginx:1.27-alpine" 'jp deploy front "{.spec.template.spec.containers[0].image}"' \
  "nginx:1.99-nexistepas n'existe pas : ErrImagePull puis ImagePullBackOff. kubectl rollout undo revient à la révision précédente." \
  "kubectl -n $NS get pods; kubectl -n $NS rollout history deploy/front"
ck_eq "3 réplicas à jour et prêts" "3/3" 'echo "$(jp deploy front "{.status.updatedReplicas}")/$(jp deploy front "{.status.readyReplicas}")"' \
  "Après le rollback, les Pods en ImagePullBackOff sont remplacés." "kubectl -n $NS rollout status deploy/front"
ck_eq "Aucun Pod en échec de téléchargement" "0" 'kn get pods --no-headers | grep -c -E "ImagePull|ErrImage"' \
  "Il ne doit plus rester de Pod de la révision cassée." "kubectl -n $NS get pods"
