## Hint 1

Copy the example NetworkPolicy from the docs and adapt it four times (one per rule).

## Hint 2

A NetworkPolicy sits on the **destination** Pods (`podSelector`) and lists the allowed sources (`from`).

## Hint 3

`kubectl -n boutique-j4 create ingress boutique --class=traefik --rule='boutique.lab.local/*=front:80'`

