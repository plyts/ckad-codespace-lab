## Hint 1

`kubectl set resources --help`

## Hint 2

QoS: `kubectl get pod … -o jsonpath='{.status.qosClass}'`.

## Hint 3

Wait for the end of the rolling update before reading the QoS.

