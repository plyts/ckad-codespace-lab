# Contrôles de d1-03 (sourcé après lib/check.sh)
ck_eq "Le CronJob backup existe" "backup" 'jp cronjob backup "{.metadata.name}"' \
  "Il faut un CronJob (batch/v1)." "kubectl -n $NS get cronjobs"
ck_eq "Planification toutes les 5 minutes" "*/5 * * * *" 'jp cronjob backup "{.spec.schedule}"' \
  "Format cron : minute heure jour mois jour-de-semaine. Toutes les 5 minutes : */5 * * * *" \
  "kubectl -n $NS get cronjob backup -o jsonpath='{.spec.schedule}'"
ck_eq "successfulJobsHistoryLimit = 2" "2" 'jp cronjob backup "{.spec.successfulJobsHistoryLimit}"' \
  "Historique des Jobs réussis (3 par défaut)." "kubectl -n $NS get cronjob backup -o yaml | grep HistoryLimit"
ck_eq "failedJobsHistoryLimit = 1" "1" 'jp cronjob backup "{.spec.failedJobsHistoryLimit}"' \
  "Historique des Jobs échoués (1 par défaut, mais explicite ici)." "kubectl -n $NS get cronjob backup -o yaml | grep HistoryLimit"
ck_eq "concurrencyPolicy = Forbid" "Forbid" 'jp cronjob backup "{.spec.concurrencyPolicy}"' \
  "Forbid saute une exécution si la précédente tourne encore (Allow par défaut, Replace remplace)." \
  "kubectl explain cronjob.spec.concurrencyPolicy"
ck_eq "Commande du conteneur" "sh -c echo sauvegarde" 'jp cronjob backup "{.spec.jobTemplate.spec.template.spec.containers[0].command[*]}{.spec.jobTemplate.spec.template.spec.containers[0].args[*]}" | xargs' \
  "La commande demandée est sh -c 'echo sauvegarde'." "kubectl -n $NS get cronjob backup -o yaml | grep -A4 command"
