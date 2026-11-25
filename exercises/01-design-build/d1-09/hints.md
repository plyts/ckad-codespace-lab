## Indice 1

Commence par le fichier : `kubectl run report --image=busybox:1.37 --dry-run=client -o yaml > ~/ckad/d1-09/report.yaml`.

## Indice 2

`emptyDir: { medium: Memory, sizeLimit: 16Mi }`.

## Indice 3

Applique le fichier enregistré : `kubectl apply -f ~/ckad/d1-09/report.yaml`.

