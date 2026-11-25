## Indice 1

`kubectl create cronjob --help` : options `--image` et `--schedule`, la commande après `--`.

## Indice 2

Les limites d'historique et `concurrencyPolicy` sont sous `spec` du CronJob : génère le YAML et ajoute-les.

## Indice 3

`kubectl -n d1-03 create cronjob backup --image=busybox:1.37 --schedule='*/5 * * * *' --dry-run=client -o yaml -- sh -c 'echo sauvegarde'`

