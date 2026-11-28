## Hint 1

`kubectl create deployment … --replicas=N` then `kubectl expose deploy … --port=… --target-port=…`: 6 commands in total.

## Hint 2

For the http-echo argument: `kubectl create deployment api --image=hashicorp/http-echo:1.0.0 --replicas=2 -- /http-echo -text='api v1'`.

## Hint 3

Test: `kubectl -n boutique-j1 run t --rm -i --image=busybox:1.37 --restart=Never -- wget -qO- http://api`.

