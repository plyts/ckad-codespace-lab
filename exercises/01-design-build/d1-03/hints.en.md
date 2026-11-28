## Hint 1

`kubectl create cronjob --help`: options `--image` and `--schedule`, the command after `--`.

## Hint 2

History limits and `concurrencyPolicy` live under the CronJob's `spec`: generate the YAML and add them.

## Hint 3

`kubectl -n d1-03 create cronjob backup --image=busybox:1.37 --schedule='*/5 * * * *' --dry-run=client -o yaml -- sh -c 'echo sauvegarde'`

