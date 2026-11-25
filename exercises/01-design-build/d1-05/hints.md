## Indice 1

Deux conteneurs, un volume `emptyDir` commun : l'init le monte sur `/work`, nginx sur `/usr/share/nginx/html`.

## Indice 2

Commande de l'init : `sh -c 'echo "site prêt" > /work/index.html'`.

## Indice 3

Pour tester : `kubectl run tmp --rm -it --image=busybox:1.37 --restart=Never -- wget -qO- http://<IP du Pod>`.

