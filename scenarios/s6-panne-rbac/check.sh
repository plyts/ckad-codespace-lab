# Contrôles de s6-panne-rbac (sourcé après lib/check.sh)
SA="system:serviceaccount:$NS:reporter"
ck_eq "list pods" "yes" 'k auth can-i list pods -n $NS --as=$SA' \
  "forbidden.log : cannot list resource \"pods\" … : il manque un Role et son RoleBinding." "kubectl -n $NS describe role,rolebinding"
ck_eq "list configmaps" "yes" 'k auth can-i list configmaps -n $NS --as=$SA' \
  "Le Role doit couvrir pods ET configmaps." "kubectl -n $NS get role reporter -o yaml"
ck_eq "Pas de lecture des Secrets" "no" 'k auth can-i get secrets -n $NS --as=$SA' \
  "Moindre privilège." "kubectl -n $NS get role reporter -o yaml"
ck_eq "Pas de suppression" "no" 'k auth can-i delete pods -n $NS --as=$SA' \
  "Lecture seulement : get, list." "kubectl -n $NS get role reporter -o yaml"
ck_eq "Role et RoleBinding nommés reporter" "reporter reporter" 'echo "$(jp role reporter "{.metadata.name}") $(jp rolebinding reporter "{.roleRef.name}")"' \
  "Le RoleBinding reporter référence le Role reporter." "kubectl -n $NS get role,rolebinding"
