## Indice 1

`kubectl create job` ne connaît pas `completions` : génère le YAML puis édite-le.

## Indice 2

Les champs `completions`, `parallelism` et `backoffLimit` sont sous `spec` du Job (pas sous `template`).

## Indice 3

`kubectl -n d1-02 create job counter --image=busybox:1.37 --dry-run=client -o yaml -- sh -c 'echo traitement terminé' > job.yaml`, puis ajoute les 3 champs.

