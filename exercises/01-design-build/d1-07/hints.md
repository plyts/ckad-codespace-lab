## Indice 1

Trois lignes à ajouter au Dockerfile : `LABEL`, `ENV`, `EXPOSE`.

## Indice 2

Construire : `docker build -t ckad/hello:v1 ~/ckad/d1-07`.

## Indice 3

Exporter : `docker save -o ~/ckad/d1-07/hello.tar ckad/hello:v1` (podman : `podman save -o …`).

