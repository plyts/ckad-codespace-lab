# Contrôles de d2-09 (sourcé après lib/check.sh)
ck_eq "Deployment prod-web créé dans d2-09" "prod-web" 'jp deploy prod-web "{.metadata.name}"' \
  "namePrefix: prod- et namespace: d2-09 dans le kustomization.yaml, puis kubectl apply -k." "kubectl -n $NS get deploy,svc"
ck_eq "3 réplicas prêts" "3" 'jp deploy prod-web "{.status.readyReplicas}"' \
  "Champ replicas: - name: web  count: 3 (le nom AVANT préfixe)." "kubectl kustomize ~/ckad/d2-09/overlays/prod | grep replicas"
ck_eq "Label env=prod sur le Deployment" "prod" 'jp deploy prod-web "{.metadata.labels.env}"' \
  "labels: - pairs: {env: prod} (ou commonLabels, déprécié mais encore accepté)." "kubectl -n $NS get deploy prod-web --show-labels"
ck_eq "Service prod-web étiqueté env=prod" "prod" 'jp svc prod-web "{.metadata.labels.env}"' \
  "Le label doit s'appliquer à toutes les ressources de la base." "kubectl -n $NS get svc --show-labels"
ck_true "Overlay enregistré au bon chemin" "grep -q 'prod-' $OUT/overlays/prod/kustomization.yaml && kubectl kustomize $OUT/overlays/prod >/dev/null" \
  "Le fichier noté est ~/ckad/d2-09/overlays/prod/kustomization.yaml et il doit être valide." "kubectl kustomize ~/ckad/d2-09/overlays/prod"
