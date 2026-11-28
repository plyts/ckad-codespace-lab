## Hint 1

`kubectl expose --help`

## Hint 2

`kubectl -n d5-01 expose deploy web --port=80 --target-port=80`

## Hint 3

Check the Endpoints: `kubectl -n d5-01 get endpointslices`.

