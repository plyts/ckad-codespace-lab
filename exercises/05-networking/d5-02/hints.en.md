## Hint 1

`kubectl expose` can create a NodePort (`--type`) but not choose its number: generate the YAML with `--dry-run=client -o yaml`.

## Hint 2

Add `nodePort: 30080` in `spec.ports[0]`, then apply.

## Hint 3

`kubectl -n d5-02 expose deploy web --name=web-np --type=NodePort --port=80 --dry-run=client -o yaml > np.yaml`

