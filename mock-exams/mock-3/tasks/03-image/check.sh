# Contrôles de m3-03 (sourcé après lib/check.sh)
ck_eq "Label team=payments" "payments" "docker image inspect ckad/m3-app:1.0 --format '{{index .Config.Labels \"team\"}}'" \
  "LABEL team=payments dans le Dockerfile, puis docker build -t ckad/m3-app:1.0." "docker images | head"
ck_match "Port 9000 exposé" "9000/tcp" "docker image inspect ckad/m3-app:1.0 --format '{{json .Config.ExposedPorts}}'" "EXPOSE 9000." "docker image inspect ckad/m3-app:1.0"
ck_true "Archive image.tar avec le tag ckad/m3-app:1.0" "tar -xOf $OUT/image.tar manifest.json | grep -q 'ckad/m3-app:1.0'" "docker save -o ~/ckad/m3-03/image.tar ckad/m3-app:1.0." "ls -l $OUT"
