# Contrôles de d2-01 (sourcé après lib/check.sh)
ck_eq "Deployment front" "front" 'jp deploy front "{.metadata.name}"' \
  "Il faut un Deployment (apps/v1), pas des Pods isolés." "kubectl -n $NS get deploy"
ck_eq "Image nginx:1.27-alpine" "nginx:1.27-alpine" 'jp deploy front "{.spec.template.spec.containers[0].image}"' \
  "L'image est dans le template des Pods." "kubectl -n $NS get deploy front -o wide"
ck_eq "Sélecteur app=front" "front" 'jp deploy front "{.spec.selector.matchLabels.app}"' \
  "kubectl create deployment front pose automatiquement app=front sur le sélecteur et les Pods." "kubectl -n $NS get deploy front -o jsonpath='{.spec.selector}'"
ck_eq "3 réplicas prêts" "3" 'jp deploy front "{.status.readyReplicas}"' \
  "Les réplicas doivent être Running et Ready." "kubectl -n $NS get rs,pods -l app=front"
