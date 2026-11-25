# Contrôles de m2-08 (sourcé après lib/check.sh)
ck_eq "Quota" "4 800m 512Mi" 'jp quota team-quota "{.spec.hard.pods} {.spec.hard.requests\.cpu} {.spec.hard.requests\.memory}"' \
  "kubectl create quota team-quota --hard=pods=4,requests.cpu=800m,requests.memory=512Mi." "kubectl -n $NS describe quota"
ck_eq "Pod probe Running, requests 100m" "Running 100m" 'jp pod probe "{.status.phase} {.spec.containers[0].resources.requests.cpu}"' \
  "Avec un quota requests.*, un Pod sans requests est refusé." "kubectl -n $NS describe quota team-quota"
ck_true "Quota utilisé" "kubectl --context $CTX -n $NS describe quota team-quota | grep -q '100m'" "Le Pod doit compter dans le quota." "kubectl -n $NS describe quota team-quota"
