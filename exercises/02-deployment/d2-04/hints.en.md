## Hint 1

Look at the Pods: `kubectl -n d2-04 get pods`, then `describe` a failing Pod.

## Hint 2

`kubectl -n d2-04 rollout history deploy/front` shows the revisions.

## Hint 3

`kubectl -n d2-04 rollout undo deploy/front`

