## Hint 1

`kubectl create cronjob --schedule=… --image=… -- sh -c 'date'`

## Hint 2

Fields to add: `concurrencyPolicy`, `successfulJobsHistoryLimit`.

## Hint 3

`kubectl create job <name> --from=cronjob/<cronjob>`

