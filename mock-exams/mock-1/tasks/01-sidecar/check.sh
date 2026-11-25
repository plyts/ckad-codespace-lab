# Contrôles de m1-01 (sourcé après lib/check.sh)
ck_eq "reader est un sidecar natif" "Always" 'jp pod audit "{.spec.initContainers[?(@.name==\"reader\")].restartPolicy}"' \
  "Sidecar natif : initContainers + restartPolicy: Always." "kubectl -n $NS get pod audit -o yaml | grep -B2 -A6 initContainers"
ck_eq "Pod Running" "Running" 'jp pod audit "{.status.phase}"' "Le Pod doit tourner." "kubectl -n $NS describe pod audit | tail"
ck_true "Les logs de reader montrent « event »" "kubectl --context $CTX -n $NS logs audit -c reader --tail=3 | grep -q event" \
  "Même volume, même chemin /var/audit dans les deux conteneurs." "kubectl -n $NS logs audit -c reader --tail=3"
