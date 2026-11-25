#!/usr/bin/env bash
# Solution de référence : m3-03 — Image de conteneur
cd ~/ckad/m3-03/app
sed -i '1a LABEL team=payments\nEXPOSE 9000' Dockerfile
cat Dockerfile
docker build -t ckad/m3-app:1.0 .
docker save -o ~/ckad/m3-03/image.tar ckad/m3-app:1.0
