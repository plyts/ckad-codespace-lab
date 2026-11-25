## Indice 1

Lis `forbidden.log` : il donne le verbe, la ressource et le namespace refusés.

## Indice 2

`kubectl -n rapports create role reporter --verb=get,list --resource=pods,configmaps`

## Indice 3

`kubectl -n rapports create rolebinding reporter --role=reporter --serviceaccount=rapports:reporter`

