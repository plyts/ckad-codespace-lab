# Contrôles de m4-01 (sourcé après lib/check.sh)
ck_eq "Pod edge prêt, image nginx:1.28-alpine" "true nginx:1.28-alpine" 'jp pod edge "{.status.containerStatuses[0].ready} {.spec.containers[0].image}"' \
  "kubectl run edge --image=nginx:1.28-alpine --labels=tier=edge,env=prod --port=80." "kubectl -n $NS get pod edge -o wide"
ck_eq "Label tier=edge" "edge" 'jp pod edge "{.metadata.labels.tier}"' "--labels=tier=edge,env=prod." "kubectl -n $NS get pod edge --show-labels"
ck_true "Manifeste enregistré" "grep -q 'name: edge' $HOME/ckad/m4-01/edge.yaml" "kubectl run … --dry-run=client -o yaml > fichier, ou kubectl get pod -o yaml > fichier." "ls -l $HOME/ckad/m4-01/edge.yaml"
