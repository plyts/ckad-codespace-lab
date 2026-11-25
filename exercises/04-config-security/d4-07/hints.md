## Indice 1

Deux objets : un Role (les droits) et un RoleBinding (qui les reçoit). Les logs sont la sous-ressource `pods/log`.

## Indice 2

`kubectl create role --help` (`--verb`, `--resource`) et `kubectl create rolebinding --help` (`--serviceaccount=<ns>:<nom>`).

## Indice 3

Teste : `kubectl auth can-i list pods -n d4-07 --as=system:serviceaccount:d4-07:monitor`.

