# Contrôles de m5-01 (sourcé après lib/check.sh)
ck_eq "completions / parallelism / backoffLimit" "3 1 1" 'jp job migrate "{.spec.completions} {.spec.parallelism} {.spec.backoffLimit}"' \
  "Trois champs sous spec du Job." "kubectl -n $NS get job migrate -o yaml | grep -E 'completions|parallelism|backoff'"
ck_eq "3 réussites" "3" 'jp job migrate "{.status.succeeded}"' "Le Job doit aller au bout." "kubectl -n $NS get pods -l job-name=migrate"
ck_true "Les logs disent « migré »" "kubectl --context $CTX -n $NS logs job/migrate | grep -q migré" "Commande demandée : echo migré." "kubectl -n $NS logs job/migrate"
