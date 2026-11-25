# Contrôles de d1-09 (sourcé après lib/check.sh)
ck_eq "Pod report prêt" "True" 'jp pod report "{.status.conditions[?(@.type==\"Ready\")].status}"' \
  "Le Pod doit tourner." "kubectl -n $NS describe pod report | tail -15"
ck_eq "Volume work en mémoire" "Memory" 'jp pod report "{.spec.volumes[?(@.name==\"work\")].emptyDir.medium}"' \
  "emptyDir.medium: Memory monte un tmpfs (RAM)." "kubectl -n $NS get pod report -o yaml | grep -A3 emptyDir"
ck_eq "Limite 16Mi" "16Mi" 'jp pod report "{.spec.volumes[?(@.name==\"work\")].emptyDir.sizeLimit}"' \
  "emptyDir.sizeLimit: 16Mi." "kubectl explain pod.spec.volumes.emptyDir"
ck_eq "Init container stamp" "stamp" 'jp pod report "{.spec.initContainers[0].name}"' \
  "L'écriture se fait dans un init container nommé stamp." "kubectl -n $NS get pod report -o jsonpath='{.spec.initContainers[*].name}'"
ck_eq "reader affiche le rapport" "rapport du jour" 'kn logs report -c reader' \
  "Le conteneur reader lit le fichier écrit par l'init : même volume, même chemin." "kubectl -n $NS logs report -c reader"
ck_true "Manifeste enregistré dans ~/ckad/d1-09/report.yaml" "grep -q 'kind: Pod' $OUT/report.yaml && grep -q 'medium: Memory' $OUT/report.yaml" \
  "À l'examen, une tâche demande souvent d'enregistrer un fichier à un chemin précis : il est noté." "cat $OUT/report.yaml"
