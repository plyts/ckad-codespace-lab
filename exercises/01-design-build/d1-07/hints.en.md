## Hint 1

Three lines to add to the Dockerfile: `LABEL`, `ENV`, `EXPOSE`.

## Hint 2

Build: `docker build -t ckad/hello:v1 ~/ckad/d1-07`.

## Hint 3

Export: `docker save -o ~/ckad/d1-07/hello.tar ckad/hello:v1` (podman: `podman save -o …`).

