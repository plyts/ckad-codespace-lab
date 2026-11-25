# Contrôles de d4-03 (sourcé après lib/check.sh)
ck_eq "ServiceAccount deployer" "deployer" 'jp sa deployer "{.metadata.name}"' \
  "kubectl create serviceaccount deployer." "kubectl -n $NS get sa"
ck_eq "Le Pod utilise deployer" "deployer" 'jp pod tool "{.spec.serviceAccountName}"' \
  "spec.serviceAccountName (le champ serviceAccount seul est déprécié)." "kubectl -n $NS get pod tool -o jsonpath='{.spec.serviceAccountName}'"
ck_eq "Jeton non monté" "false" 'jp pod tool "{.spec.automountServiceAccountToken}"' \
  "automountServiceAccountToken: false dans le Pod (ou sur le ServiceAccount)." "kubectl -n $NS get pod tool -o yaml | grep -i automount"
ck_eq "Pod prêt" "true" 'jp pod tool "{.status.containerStatuses[0].ready}"' \
  "Le Pod doit tourner." "kubectl -n $NS describe pod tool | tail"
