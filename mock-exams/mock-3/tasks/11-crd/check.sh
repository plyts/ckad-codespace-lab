# Contrôles de m3-11 (sourcé après lib/check.sh)
ck_eq "Maintenance weekly" "dimanche 02h" 'jp maintenances.ops.m3.lab weekly "{.spec.window}"' "apiVersion: ops.m3.lab/v1alpha1 (version servie par la CRD)." "kubectl api-resources --api-group=ops.m3.lab; kubectl explain maintenance.spec"
ck_true "resources.txt" "grep -q maintenances $OUT/resources.txt" "kubectl api-resources --api-group=ops.m3.lab > fichier." "cat $OUT/resources.txt"
