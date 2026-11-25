# Contrôles de m3-09 (sourcé après lib/check.sh)
ck_eq "Template : serviceAccountName metrics-reader" "metrics-reader" 'jp deploy collector "{.spec.template.spec.serviceAccountName}"' \
  "kubectl set serviceaccount deploy/collector metrics-reader." "kubectl -n $NS get deploy collector -o yaml | grep serviceAccount"
ck_eq "Pods en cours sous metrics-reader" "metrics-reader" 'kn get pods -l app=collector --field-selector=status.phase=Running -o jsonpath="{.items[0].spec.serviceAccountName}"' "Le rolling update remplace les Pods." "kubectl -n $NS get pods -o custom-columns=NAME:.metadata.name,SA:.spec.serviceAccountName"
