## Hint 1

`kubectl create job` does not know `completions`: generate the YAML then edit it.

## Hint 2

`completions`, `parallelism` and `backoffLimit` live under the Job's `spec` (not under `template`).

## Hint 3

`kubectl -n d1-02 create job counter --image=busybox:1.37 --dry-run=client -o yaml -- sh -c 'echo traitement terminé' > job.yaml`, then add the 3 fields.

