# Contrôles de m4-02 (sourcé après lib/check.sh)
ck_eq "Un Pod prêt par nœud" "$(k get nodes --no-headers | wc -l | tr -d ' ')" 'jp ds log-agent "{.status.numberReady}"' \
  "Toleration node-role.kubernetes.io/control-plane:NoSchedule pour le control-plane." "kubectl -n $NS get pods -o wide; kubectl describe nodes | grep Taints"
