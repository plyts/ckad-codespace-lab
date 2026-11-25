# Contrôles de m5-07 (sourcé après lib/check.sh)
ck_eq "1 réplica disponible" "1" 'jp deploy notifier "{.status.availableReplicas}"' \
  "Exit code 3 : /config/ready manque. Volume configMap notifier-config monté sur /config." "kubectl -n $NS describe pod -l app=notifier | grep -A4 'Last State'"
ck_match "Commande inchangée" "test -f /config/ready" 'jp deploy notifier "{.spec.template.spec.containers[0].command[*]}"' "La consigne interdit de changer la commande." "kubectl -n $NS get deploy notifier -o yaml | grep -A3 command"
ck_eq "ConfigMap montée" "notifier-config" 'jp deploy notifier "{.spec.template.spec.volumes[0].configMap.name}"' "volumes[].configMap.name." "kubectl -n $NS get deploy notifier -o yaml | grep -A3 volumes"
