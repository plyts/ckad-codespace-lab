## Hint 1

Two containers, one shared `emptyDir` volume: the init mounts it on `/work`, nginx on `/usr/share/nginx/html`.

## Hint 2

Init command: `sh -c 'echo "site prêt" > /work/index.html'`.

## Hint 3

To test: `kubectl run tmp --rm -it --image=busybox:1.37 --restart=Never -- wget -qO- http://<Pod IP>`.

