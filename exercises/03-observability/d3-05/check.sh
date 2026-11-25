# Contrôles de d3-05 (sourcé après lib/check.sh)
ck_eq "Image redis:7.4-alpine" "redis:7.4-alpine" 'jp deploy cache "{.spec.template.spec.containers[0].image}"' \
  "Le tag 7.4-alpinee n'existe pas : ErrImagePull puis ImagePullBackOff (le kubelet espace ses essais)." \
  "kubectl -n $NS describe pod -l app=cache | grep -A3 -i events"
ck_eq "1 réplica prêt" "1" 'jp deploy cache "{.status.readyReplicas}"' \
  "Le nouveau Pod doit démarrer." "kubectl -n $NS get pods"
