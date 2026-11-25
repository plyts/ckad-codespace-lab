# Contrôles de m5-02 (sourcé après lib/check.sh)
ck_eq "PVC media-pvc Bound, 150Mi" "Bound 150Mi" 'jp pvc media-pvc "{.status.phase} {.spec.resources.requests.storage}"' \
  "WaitForFirstConsumer : Bound dès qu'un Pod l'utilise." "kubectl -n $NS describe pvc media-pvc | tail -4"
ck_eq "Le Pod monte le PVC" "media-pvc" 'jp pod media "{.spec.volumes[?(@.persistentVolumeClaim)].persistentVolumeClaim.claimName}"' \
  "volumes[].persistentVolumeClaim.claimName." "kubectl -n $NS get pod media -o yaml | grep -A3 volumes"
ck_eq "Fichier écrit" "photo" 'kn exec media -- cat /media/data.txt' "Monté sur /media." "kubectl -n $NS exec media -- ls /media"
