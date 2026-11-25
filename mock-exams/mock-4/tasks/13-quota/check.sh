# Contrôles de m4-13 (sourcé après lib/check.sh)
ck_eq "Quota" "6 1 1Gi" 'jp quota team-quota "{.spec.hard.pods} {.spec.hard.requests\.cpu} {.spec.hard.requests\.memory}"' \
  "kubectl create quota team-quota --hard=pods=6,requests.cpu=1,requests.memory=1Gi." "kubectl -n $NS describe quota"
ck_eq "Pod probe Running, requests 100m" "Running 100m" 'jp pod probe "{.status.phase} {.spec.containers[0].resources.requests.cpu}"' \
  "Avec un quota requests.*, un Pod sans requests est refusé." "kubectl -n $NS describe quota team-quota"
ck_true "Quota utilisé" "kubectl --context $CTX -n $NS describe quota team-quota | grep -q '100m'" "Le Pod doit compter dans le quota." "kubectl -n $NS describe quota team-quota"
