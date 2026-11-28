## Hint 1

`kubectl -n d3-04 get pods`, then `kubectl -n d3-04 describe pod <pod>`: look at "Last State".

## Hint 2

`kubectl -n d3-04 logs <pod> --previous` shows the output of the dead container.

## Hint 3

`kubectl -n d3-04 edit deploy worker` and fix `slep` into `sleep`.

