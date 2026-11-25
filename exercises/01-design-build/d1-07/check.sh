# Contrôles de d1-07 (sourcé après lib/check.sh)
ck_true "L'image ckad/hello:v1 existe" "docker image inspect ckad/hello:v1" \
  "L'image doit être construite avec le tag exact ckad/hello:v1 (option -t)." "docker images | grep ckad"
ck_eq "Label maintainer=ckad" "ckad" "docker image inspect ckad/hello:v1 --format '{{index .Config.Labels \"maintainer\"}}'" \
  "Instruction Dockerfile : LABEL maintainer=ckad, puis reconstruire." "docker image inspect ckad/hello:v1 --format '{{json .Config.Labels}}'"
ck_match "Variable APP_VERSION=v1" "APP_VERSION=v1" "docker image inspect ckad/hello:v1 --format '{{json .Config.Env}}'" \
  "Instruction Dockerfile : ENV APP_VERSION=v1." "docker image inspect ckad/hello:v1 --format '{{json .Config.Env}}'"
ck_match "Port 8080 exposé" "8080/tcp" "docker image inspect ckad/hello:v1 --format '{{json .Config.ExposedPorts}}'" \
  "Instruction Dockerfile : EXPOSE 8080." "docker image inspect ckad/hello:v1 --format '{{json .Config.ExposedPorts}}'"
ck_true "Archive ~/ckad/d1-07/hello.tar contenant ckad/hello:v1" "tar -xOf $OUT/hello.tar manifest.json | grep -q 'ckad/hello:v1'" \
  "docker save -o fichier.tar image:tag écrit l'image et son tag dans l'archive." "ls -l $OUT; tar -tf $OUT/hello.tar | head"
