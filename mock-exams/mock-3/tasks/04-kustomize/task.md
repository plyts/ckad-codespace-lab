---
id: m3-04
title: Overlay Kustomize
domain: 2
level: examen
context: ckad-a
namespace: m3-04
time: 8
doc: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
skill: kustomize
weight: 7
---
Base Kustomize : `~/ckad/m3-04/base`. Crée l'overlay `~/ckad/m3-04/overlay` qui déploie dans
`m3-04`, préfixe les noms par `stg-`, fixe **2 réplicas**, ajoute le label
`tier=staging`, et remplace l'image par `nginx:1.28-alpine`. Applique-le.
