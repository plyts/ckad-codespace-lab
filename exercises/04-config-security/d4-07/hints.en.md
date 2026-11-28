## Hint 1

Two objects: a Role (the permissions) and a RoleBinding (who receives them). Logs are the `pods/log` subresource.

## Hint 2

`kubectl create role --help` (`--verb`, `--resource`) and `kubectl create rolebinding --help` (`--serviceaccount=<ns>:<name>`).

## Hint 3

Test: `kubectl auth can-i list pods -n d4-07 --as=system:serviceaccount:d4-07:monitor`.

