# Contrôles de d3-04 (sourcé après lib/check.sh)
ck_eq "Code de sortie 127 noté" "127" 'tr -d "[:space:]" < $OUT/exit-code.txt' \
  "describe pod montre Last State: Terminated, Exit Code. 127 = commande introuvable (slep)." \
  "kubectl -n $NS describe pod -l app=worker | grep -A4 'Last State'"
ck_eq "1 réplica disponible" "1" 'jp deploy worker "{.status.availableReplicas}"' \
  "La commande doit être sleep 3600 (faute de frappe : slep)." "kubectl -n $NS logs deploy/worker --previous"
ck_eq "Plus de Pod en CrashLoopBackOff" "0" 'kn get pods --no-headers | grep -c -E "CrashLoop|Error"' \
  "Les anciens Pods disparaissent une fois le rolling update terminé." "kubectl -n $NS get pods"
