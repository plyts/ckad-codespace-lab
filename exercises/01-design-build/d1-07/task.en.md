---
id: d1-07
title: Build and export an image
---
Directory `~/ckad/d1-07/` contains a `Dockerfile` and an `index.html`.

1. Edit the `Dockerfile` to add the label `maintainer=ckad`, the environment variable
   `APP_VERSION=v1` and declare port `8080`.
2. Build the image `ckad/hello:v1` with `docker` (or `podman`).
3. Export it into the archive `~/ckad/d1-07/hello.tar`.

(Context and namespace do not apply: this task happens outside the cluster.)
