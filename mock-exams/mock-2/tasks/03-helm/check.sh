# Contrôles de m2-03 (sourcé après lib/check.sh)
ck_eq "Révision 2 déployée" "2" 'helm --kube-context "$CTX" -n "$NS" status blog -o json | python3 -c "import sys,json;print(json.load(sys.stdin)[\"version\"])"' \
  "helm upgrade blog <chart> --set …" "helm -n $NS history blog"
ck_eq "3 réplicas prêts" "3" 'jp deploy blog-webapp "{.status.readyReplicas}"' "--set replicaCount=3." "helm -n $NS get values blog"
ck_eq "MESSAGE" "v2" 'jp deploy blog-webapp "{.spec.template.spec.containers[0].env[0].value}"' "--set message=v2." "helm -n $NS get values blog"
ck_true "history.txt" "grep -qi 'upgrade' $OUT/history.txt" "helm history blog > ~/ckad/m2-03/history.txt." "cat $OUT/history.txt"
