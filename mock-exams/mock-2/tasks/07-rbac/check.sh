# Contrôles de m2-07 (sourcé après lib/check.sh)
SA="system:serviceaccount:$NS:auditor"
for v in $(echo get,list,watch | tr , ' '); do
  ck_eq "auditor peut $v deployments" "yes" "k auth can-i $v deployments -n $NS --as=$SA" "Role auditor-role + RoleBinding auditor-binding." "kubectl -n $NS describe role,rolebinding"
done
ck_eq "auditor ne peut pas delete deployments" "no" 'k auth can-i delete deployments -n $NS --as=$SA' "Moindre privilège." "kubectl -n $NS get role auditor-role -o yaml"
