# Contrôles de d4-02 (sourcé après lib/check.sh)
ck_eq "Secret db-cred (password)" "S3cr3t!" 'jp secret db-cred "{.data.password}" | base64 -d' \
  "Dans un Secret, data est encodé en base64 (pas chiffré !). Attention aux guillemets autour de S3cr3t! en bash." \
  "kubectl -n $NS get secret db-cred -o jsonpath='{.data.password}' | base64 -d"
ck_eq "Secret db-cred (username)" "admin" 'jp secret db-cred "{.data.username}" | base64 -d' \
  "--from-literal=username=admin." "kubectl -n $NS describe secret db-cred"
ck_eq "DB_PASSWORD référence le Secret" "db-cred/password" 'jp pod db-client "{.spec.containers[0].env[?(@.name==\"DB_PASSWORD\")].valueFrom.secretKeyRef.name}/{.spec.containers[0].env[?(@.name==\"DB_PASSWORD\")].valueFrom.secretKeyRef.key}"' \
  "env: - name: DB_PASSWORD  valueFrom: secretKeyRef: {name: db-cred, key: password}" "kubectl -n $NS get pod db-client -o yaml | grep -A5 env"
ck_eq "Valeur dans le conteneur" "S3cr3t!" 'kn exec db-client -- printenv DB_PASSWORD' \
  "Le conteneur voit la valeur décodée." "kubectl -n $NS exec db-client -- printenv DB_PASSWORD"
