# Contrôles de m4-11 (sourcé après lib/check.sh)
SA="system:serviceaccount:$NS:deployer"
for v in $(echo get,list,create,update | tr , ' '); do
  ck_eq "deployer peut $v deployments" "yes" "k auth can-i $v deployments -n $NS --as=$SA" "Role deployer-role + RoleBinding deployer-binding." "kubectl -n $NS describe role,rolebinding"
done
ck_eq "deployer ne peut pas delete pods" "no" 'k auth can-i delete pods -n $NS --as=$SA' "Moindre privilège." "kubectl -n $NS get role deployer-role -o yaml"
