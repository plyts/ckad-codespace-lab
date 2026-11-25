# Contrôles de d1-02 (sourcé après lib/check.sh)
ck_eq "Le Job counter existe" "counter" 'jp job counter "{.metadata.name}"' \
  "Il faut un objet Job (batch/v1), pas un Pod." "kubectl -n $NS get jobs"
ck_eq "completions = 3" "3" 'jp job counter "{.spec.completions}"' \
  "completions = nombre de Pods qui doivent réussir." "kubectl -n $NS get job counter -o yaml | grep -E 'completions|parallelism'"
ck_eq "parallelism = 2" "2" 'jp job counter "{.spec.parallelism}"' \
  "parallelism = nombre maximum de Pods simultanés." "kubectl -n $NS get job counter -o jsonpath='{.spec.parallelism}'"
ck_eq "backoffLimit = 2" "2" 'jp job counter "{.spec.backoffLimit}"' \
  "backoffLimit limite les relances en cas d'échec (6 par défaut)." "kubectl -n $NS get job counter -o jsonpath='{.spec.backoffLimit}'"
ck_eq "3 Pods ont réussi" "3" 'jp job counter "{.status.succeeded}"' \
  "Le Job doit aller au bout. Si un Pod échoue, lis ses logs." "kubectl -n $NS get pods -l job-name=counter; kubectl -n $NS logs -l job-name=counter"
