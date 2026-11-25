# Contrôles de m4-05 (sourcé après lib/check.sh)
ck_eq "Révision 2 déployée" "2" 'helm --kube-context "$CTX" -n "$NS" status wiki -o json | python3 -c "import sys,json;print(json.load(sys.stdin)[\"version\"])"' \
  "helm upgrade wiki <chart> --set …" "helm -n $NS history wiki"
ck_eq "2 réplicas prêts" "2" 'jp deploy wiki-webapp "{.status.readyReplicas}"' "--set replicaCount=2." "helm -n $NS get values wiki"
ck_eq "MESSAGE" "maj" 'jp deploy wiki-webapp "{.spec.template.spec.containers[0].env[0].value}"' "--set message=maj." "helm -n $NS get values wiki"
ck_true "history.txt" "grep -qi 'upgrade' $OUT/history.txt" "helm history wiki > ~/ckad/m4-05/history.txt." "cat $OUT/history.txt"
