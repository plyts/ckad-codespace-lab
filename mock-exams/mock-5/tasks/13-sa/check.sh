# Contrôles de m5-13 (sourcé après lib/check.sh)
ck_eq "Template : serviceAccountName uploader" "uploader" 'jp deploy ingest "{.spec.template.spec.serviceAccountName}"' \
  "kubectl set serviceaccount deploy/ingest uploader." "kubectl -n $NS get deploy ingest -o yaml | grep serviceAccount"
ck_eq "Pods en cours sous uploader" "uploader" 'kn get pods -l app=ingest --field-selector=status.phase=Running -o jsonpath="{.items[0].spec.serviceAccountName}"' "Le rolling update remplace les Pods." "kubectl -n $NS get pods -o custom-columns=NAME:.metadata.name,SA:.spec.serviceAccountName"
