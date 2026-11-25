## Indice 1

`kubectl create cronjob --schedule=… --image=… -- sh -c 'date'`

## Indice 2

Champs à ajouter : `concurrencyPolicy`, `successfulJobsHistoryLimit`.

## Indice 3

`kubectl create job <nom> --from=cronjob/<cronjob>`

