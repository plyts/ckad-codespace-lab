# Contrôles de d4-07 (sourcé après lib/check.sh)
SA="system:serviceaccount:$NS:monitor"
ck_eq "monitor peut lister les Pods" "yes" 'k auth can-i list pods -n $NS --as=$SA' \
  "Role avec verbs get,list,watch sur pods, lié au ServiceAccount par un RoleBinding." "kubectl -n $NS describe role pod-reader; kubectl -n $NS describe rolebinding monitor-pod-reader"
ck_eq "monitor peut lire les logs" "yes" 'k auth can-i get pods/log -n $NS --as=$SA' \
  "Les logs sont une sous-ressource : pods/log." "kubectl -n $NS describe role pod-reader"
ck_eq "monitor ne peut pas supprimer de Pod" "no" 'k auth can-i delete pods -n $NS --as=$SA' \
  "Principe du moindre privilège : seulement la lecture." "kubectl -n $NS get role pod-reader -o yaml"
ck_eq "monitor ne voit pas les Secrets" "no" 'k auth can-i get secrets -n $NS --as=$SA' \
  "Le Role ne doit couvrir que pods et pods/log." "kubectl -n $NS get role pod-reader -o yaml"
ck_eq "Droits limités au namespace" "no" 'k auth can-i list pods -n default --as=$SA' \
  "Un Role + RoleBinding ne vaut que dans son namespace (ClusterRole + ClusterRoleBinding pour tout le cluster)." "kubectl get clusterrolebindings | grep monitor"
