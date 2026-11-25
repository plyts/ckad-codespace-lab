# Contrôles de d1-01 (sourcé après lib/check.sh)
ck_eq "Le Pod web existe" "web" 'jp pod web "{.metadata.name}"' \
  "La consigne demande un Pod nommé exactement web, dans le namespace $NS." "kubectl -n $NS get pods"
ck_eq "Image nginx:1.27-alpine" "nginx:1.27-alpine" 'jp pod web "{.spec.containers[0].image}"' \
  "Le tag fait partie de l'image : nginx sans tag tire latest, pas 1.27-alpine." \
  "kubectl -n $NS get pod web -o jsonpath='{.spec.containers[0].image}'"
ck_eq "Label app=web" "web" 'jp pod web "{.metadata.labels.app}"' \
  "Les labels servent aux sélecteurs (Services, Deployments). kubectl run --labels=app=web ou kubectl label." \
  "kubectl -n $NS get pod web --show-labels"
ck_eq "Port de conteneur 80 déclaré" "80" 'jp pod web "{.spec.containers[0].ports[0].containerPort}"' \
  "containerPort est informatif mais attendu ici : kubectl run --port=80 le renseigne." \
  "kubectl -n $NS get pod web -o yaml | grep -A3 ports"
ck_eq "Le Pod est prêt" "true" 'jp pod web "{.status.containerStatuses[0].ready}"' \
  "Un Pod créé n'est pas forcément démarré : regarde les événements s'il reste Pending ou en erreur." \
  "kubectl -n $NS describe pod web | tail -15"
