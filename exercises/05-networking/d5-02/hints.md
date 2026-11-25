## Indice 1

`kubectl -n d5-02 expose deploy web --name=web-np --type=NodePort --port=80 --dry-run=client -o yaml > np.yaml`

## Indice 2

Ajoute `nodePort: 30080` dans `spec.ports[0]`.

## Indice 3

Test : `wget -qO- http://<InternalIP d'un nœud>:30080` depuis un Pod.

