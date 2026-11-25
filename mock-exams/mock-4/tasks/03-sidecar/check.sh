# Contrôles de m4-03 (sourcé après lib/check.sh)
ck_eq "reader est un sidecar natif" "Always" 'jp pod trail "{.spec.initContainers[?(@.name==\"reader\")].restartPolicy}"' \
  "Sidecar natif : initContainers + restartPolicy: Always." "kubectl -n $NS get pod trail -o yaml | grep -B2 -A6 initContainers"
ck_eq "Pod Running" "Running" 'jp pod trail "{.status.phase}"' "Le Pod doit tourner." "kubectl -n $NS describe pod trail | tail"
ck_true "Les logs de reader montrent « trace »" "kubectl --context $CTX -n $NS logs trail -c reader --tail=3 | grep -q trace" \
  "Même volume, même chemin /trail dans les deux conteneurs." "kubectl -n $NS logs trail -c reader --tail=3"
