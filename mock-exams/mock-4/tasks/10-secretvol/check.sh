# Contrôles de m4-10 (sourcé après lib/check.sh)
ck_eq "Fichier /etc/creds/pass" "Zx9-k2" 'kn exec deploy/mailer -- cat /etc/creds/pass' "Un volume secret crée un fichier par clé." "kubectl -n $NS exec deploy/mailer -- ls /etc/creds"
ck_eq "Montage en lecture seule" "true" 'jp deploy mailer "{.spec.template.spec.containers[0].volumeMounts[?(@.mountPath==\"/etc/creds\")].readOnly}"' "volumeMounts[].readOnly: true." "kubectl -n $NS get deploy mailer -o yaml | grep -A4 volumeMounts"
