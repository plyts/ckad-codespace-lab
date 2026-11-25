# Contrôles de m3-01 (sourcé après lib/check.sh)
ck_eq "completions / parallelism / backoffLimit" "4 2 1" 'jp job resize "{.spec.completions} {.spec.parallelism} {.spec.backoffLimit}"' \
  "Trois champs sous spec du Job." "kubectl -n $NS get job resize -o yaml | grep -E 'completions|parallelism|backoff'"
ck_eq "4 réussites" "4" 'jp job resize "{.status.succeeded}"' "Le Job doit aller au bout." "kubectl -n $NS get pods -l job-name=resize"
ck_true "Les logs disent « redimensionné »" "kubectl --context $CTX -n $NS logs job/resize | grep -q redimensionné" "Commande demandée : echo redimensionné." "kubectl -n $NS logs job/resize"
