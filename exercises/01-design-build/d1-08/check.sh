# Contrôles de d1-08 (sourcé après lib/check.sh)
ck_eq "Le DaemonSet node-agent existe" "node-agent" 'jp ds node-agent "{.metadata.name}"' \
  "Il faut un DaemonSet (apps/v1)." "kubectl -n $NS get ds"
ck_eq "Un Pod prévu sur chaque nœud" "$(k get nodes --no-headers | wc -l | tr -d ' ')" 'jp ds node-agent "{.status.desiredNumberScheduled}"' \
  "Le control-plane porte le taint node-role.kubernetes.io/control-plane:NoSchedule : sans toleration, le DaemonSet l'évite." \
  "kubectl describe node ckad-a-control-plane | grep -i taint"
ck_eq "Tous les Pods sont prêts" "$(k get nodes --no-headers | wc -l | tr -d ' ')" 'jp ds node-agent "{.status.numberReady}"' \
  "Chaque Pod du DaemonSet doit être Ready." "kubectl -n $NS get pods -o wide"
