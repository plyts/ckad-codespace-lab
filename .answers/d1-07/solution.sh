#!/usr/bin/env bash
# Solution de référence : d1-07 — Construire et exporter une image
cd ~/ckad/d1-07
cat > Dockerfile <<'EOF'
FROM busybox:1.37
LABEL maintainer=ckad
ENV APP_VERSION=v1
COPY index.html /www/index.html
EXPOSE 8080
CMD ["httpd", "-f", "-p", "8080", "-h", "/www"]
EOF
docker build -t ckad/hello:v1 .
docker save -o ~/ckad/d1-07/hello.tar ckad/hello:v1
# Vérification à la main
docker image inspect ckad/hello:v1 --format '{{json .Config.Labels}} {{json .Config.Env}}'
# VARIANTE podman (identique) : podman build -t ckad/hello:v1 . && podman save -o hello.tar ckad/hello:v1
