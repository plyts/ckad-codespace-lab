# Contrôles de d1-06 (sourcé après lib/check.sh)
ck_eq "PVC data Bound" "Bound" 'jp pvc data "{.status.phase}"' \
  "Avec la StorageClass standard de kind (WaitForFirstConsumer), le PVC reste Pending tant qu'aucun Pod ne l'utilise." \
  "kubectl -n $NS get pvc data; kubectl -n $NS describe pvc data | tail -5"
ck_eq "Taille demandée 100Mi" "100Mi" 'jp pvc data "{.spec.resources.requests.storage}"' \
  "La taille demandée est sous spec.resources.requests.storage." "kubectl -n $NS get pvc data -o yaml | grep storage"
ck_eq "Mode ReadWriteOnce" "ReadWriteOnce" 'jp pvc data "{.spec.accessModes[0]}"' \
  "accessModes est une liste : [ReadWriteOnce]." "kubectl -n $NS get pvc data -o jsonpath='{.spec.accessModes}'"
ck_eq "Le Pod writer utilise le PVC data" "data" 'jp pod writer "{.spec.volumes[?(@.persistentVolumeClaim)].persistentVolumeClaim.claimName}"' \
  "Le volume du Pod référence le PVC via persistentVolumeClaim.claimName." "kubectl -n $NS get pod writer -o yaml | grep -A3 volumes"
ck_eq "Fichier /data/proof.txt écrit" "persistant" 'kn exec writer -- cat /data/proof.txt' \
  "Le volume doit être monté sur /data dans le conteneur." "kubectl -n $NS exec writer -- ls -l /data"
