## Hint 1

`kubectl -n boutique-j3 get pods -l app=api` then `kubectl -n boutique-j3 logs <failing-pod>`.

## Hint 2

`kubectl -n boutique-j3 rollout history deploy/api`: each revision's cause is shown.

## Hint 3

`kubectl -n boutique-j3 rollout undo deploy/api`

