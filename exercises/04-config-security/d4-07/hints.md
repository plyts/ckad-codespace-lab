## Indice 1

`kubectl create role pod-reader --verb=get,list,watch --resource=pods,pods/log -n d4-07`

## Indice 2

`kubectl create rolebinding --help` : option `--serviceaccount=<ns>:<nom>`.

## Indice 3

Teste : `kubectl auth can-i list pods -n d4-07 --as=system:serviceaccount:d4-07:monitor`.

