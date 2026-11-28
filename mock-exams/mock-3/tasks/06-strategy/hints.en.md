## Hint 1

`kubectl edit deploy …`: `strategy: {type: Recreate}`.

## Hint 2

Remove the `rollingUpdate` block at the same time.

## Hint 3

Then `kubectl set image`.

