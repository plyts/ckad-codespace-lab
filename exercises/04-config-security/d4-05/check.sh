# Contrôles de d4-05 (sourcé après lib/check.sh)
ck_eq "Quota : pods=5" "5" 'jp quota ns-quota "{.spec.hard.pods}"' \
  "kubectl create quota ns-quota --hard=pods=5,requests.cpu=1,..." "kubectl -n $NS describe quota ns-quota"
ck_eq "Quota : requests et limits" "1 1Gi 2 2Gi" 'jp quota ns-quota "{.spec.hard.requests\.cpu} {.spec.hard.requests\.memory} {.spec.hard.limits\.cpu} {.spec.hard.limits\.memory}"' \
  "Les clés du quota contiennent un point : requests.cpu." "kubectl -n $NS get quota ns-quota -o yaml"
ck_eq "LimitRange : requests par défaut" "50m 32Mi" 'jp limitrange defaults "{.spec.limits[0].defaultRequest.cpu} {.spec.limits[0].defaultRequest.memory}"' \
  "defaultRequest = requests injectées si absentes." "kubectl -n $NS describe limitrange defaults"
ck_eq "LimitRange : limits par défaut" "100m 64Mi" 'jp limitrange defaults "{.spec.limits[0].default.cpu} {.spec.limits[0].default.memory}"' \
  "default = limits injectées si absentes (type: Container)." "kubectl -n $NS describe limitrange defaults"
ck_eq "Le Pod plain a reçu les valeurs par défaut" "50m 64Mi" 'jp pod plain "{.spec.containers[0].resources.requests.cpu} {.spec.containers[0].resources.limits.memory}"' \
  "Avec un quota sur requests/limits, un Pod sans ressources est REFUSÉ… sauf si une LimitRange les injecte. Crée la LimitRange avant le Pod." \
  "kubectl -n $NS get pod plain -o yaml | grep -A6 resources"
