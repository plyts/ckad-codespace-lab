## Hint 1

Start with the file: `kubectl run report --image=busybox:1.37 --dry-run=client -o yaml > ~/ckad/d1-09/report.yaml`.

## Hint 2

`emptyDir: { medium: Memory, sizeLimit: 16Mi }`.

## Hint 3

Apply the saved file: `kubectl apply -f ~/ckad/d1-09/report.yaml`.

