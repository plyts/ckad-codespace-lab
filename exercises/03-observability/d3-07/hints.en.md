## Hint 1

`kubectl apply -f ~/ckad/d3-07/old.yaml`: read the error message carefully.

## Hint 2

`kubectl api-resources | grep -E 'cronjob|poddisruption'` gives the current group/version.

## Hint 3

`kubectl explain cronjob` prints the VERSION at the top.

