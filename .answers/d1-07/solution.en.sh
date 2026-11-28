#!/usr/bin/env bash
# Reference solution: d1-07 — Build and export an image
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
# Manual check
docker image inspect ckad/hello:v1 --format '{{json .Config.Labels}} {{json .Config.Env}}'
# podman VARIANT (identical): podman build -t ckad/hello:v1 . && podman save -o hello.tar ckad/hello:v1
