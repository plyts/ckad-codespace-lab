# Contrôles de s5-pannes (sourcé après lib/check.sh)
ck_eq "orders prêt" "1" 'jp deploy orders "{.status.readyReplicas}"' \
  "CreateContainerConfigError : la clé DB_HOST manque dans orders-config (elle s'appelle DBHOST)." "kubectl -n $NS describe pod -l app=orders | tail -5"
ck_eq "orders-config contient DB_HOST" "db" 'jp cm orders-config "{.data.DB_HOST}"' \
  "La consigne demande de corriger la ConfigMap." "kubectl -n $NS get cm orders-config -o yaml"
ck_http "payments répond" "$NS" "" "http://payments.$NS" "payments ok" \
  "Le sélecteur du Service (app=payment) ne correspond pas aux Pods (app=payments) : aucun Endpoint." "kubectl -n $NS get endpointslices -l kubernetes.io/service-name=payments"
ck_eq "PVC uploads Bound" "Bound" 'jp pvc uploads "{.status.phase}"' \
  "La StorageClass fast n'existe pas (kubectl get storageclass). storageClassName est immuable : recrée le PVC." "kubectl get storageclass; kubectl -n $NS describe pvc uploads | tail -4"
ck_eq "uploader Running" "Running" 'jp pod uploader "{.status.phase}"' \
  "Le Pod attend son PVC ; recrée-le s'il reste bloqué." "kubectl -n $NS describe pod uploader | tail -5"
