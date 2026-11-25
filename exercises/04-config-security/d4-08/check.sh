# Contrôles de d4-08 (sourcé après lib/check.sh)
ck_eq "Backup nightly existe" "nightly" 'jp backups.lab.ckad.io nightly "{.metadata.name}"' \
  "La CRD définit le kind Backup du groupe lab.ckad.io, version v1 (apiVersion: lab.ckad.io/v1)." "kubectl api-resources --api-group=lab.ckad.io"
ck_eq "schedule et retention" "0 2 * * * 7" 'jp backups.lab.ckad.io nightly "{.spec.schedule} {.spec.retention}"' \
  "retention est un entier (pas de guillemets), schedule une chaîne." "kubectl explain backup.spec"
