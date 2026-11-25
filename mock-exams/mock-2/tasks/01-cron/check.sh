# Contrôles de m2-01 (sourcé après lib/check.sh)
ck_eq "Planification" "30 1 * * *" 'jp cronjob report "{.spec.schedule}"' "spec.schedule." "kubectl -n $NS get cronjob report"
ck_eq "Politique et historique" "Replace 5" 'jp cronjob report "{.spec.concurrencyPolicy} {.spec.successfulJobsHistoryLimit}"' \
  "concurrencyPolicy et successfulJobsHistoryLimit sous spec du CronJob." "kubectl -n $NS get cronjob report -o yaml | grep -E 'concurrency|History'"
ck_eq "Job report-manual créé depuis le CronJob" "1" 'jp job report-manual "{.status.succeeded}"' \
  "kubectl create job report-manual --from=cronjob/report." "kubectl -n $NS get jobs"
