# Contrôles de m5-12 (sourcé après lib/check.sh)
ck_eq "Pipeline nightly-etl" "s3-bucket" 'jp pipelines.data.m5.lab nightly-etl "{.spec.source}"' "apiVersion: data.m5.lab/v1alpha1 (version servie par la CRD)." "kubectl api-resources --api-group=data.m5.lab; kubectl explain pipeline.spec"
ck_true "resources.txt" "grep -q pipelines $OUT/resources.txt" "kubectl api-resources --api-group=data.m5.lab > fichier." "cat $OUT/resources.txt"
