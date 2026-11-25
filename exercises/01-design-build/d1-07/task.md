---
id: d1-07
title: Construire et exporter une image
domain: 1
level: avance
context: ckad-a
namespace: d1-07
time: 8
doc: https://docs.docker.com/reference/dockerfile/
skill: images
---
Le dossier `~/ckad/d1-07/` contient un `Dockerfile` et un `index.html`.

1. Modifie le `Dockerfile` pour ajouter le label `maintainer=ckad`, la variable
   d'environnement `APP_VERSION=v1` et déclarer le port `8080`.
2. Construis l'image `ckad/hello:v1` avec `docker` (ou `podman`).
3. Exporte-la dans l'archive `~/ckad/d1-07/hello.tar`.

(Contexte et namespace sans objet : cette tâche se fait hors du cluster.)
