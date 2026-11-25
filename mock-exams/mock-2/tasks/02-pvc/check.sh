# Contrôles de m2-02 (sourcé après lib/check.sh)
ck_eq "PVC cache-pvc Bound, 200Mi" "Bound 200Mi" 'jp pvc cache-pvc "{.status.phase} {.spec.resources.requests.storage}"' \
  "WaitForFirstConsumer : Bound dès qu'un Pod l'utilise." "kubectl -n $NS describe pvc cache-pvc | tail -4"
ck_eq "Le Pod monte le PVC" "cache-pvc" 'jp pod cache "{.spec.volumes[?(@.persistentVolumeClaim)].persistentVolumeClaim.claimName}"' \
  "volumes[].persistentVolumeClaim.claimName." "kubectl -n $NS get pod cache -o yaml | grep -A3 volumes"
ck_eq "Fichier écrit" "chaud" 'kn exec cache -- cat /cache/data.txt' "Monté sur /cache." "kubectl -n $NS exec cache -- ls /cache"
