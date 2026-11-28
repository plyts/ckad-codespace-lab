## Hint 1

Read `forbidden.log`: it gives the denied verb, resource and namespace.

## Hint 2

`kubectl -n rapports create role reporter --verb=get,list --resource=pods,configmaps`

## Hint 3

`kubectl -n rapports create rolebinding reporter --role=reporter --serviceaccount=rapports:reporter`

