---
id: m5-04
title: Kustomize
domain: 2
level: examen
context: ckad-b
namespace: m5-04
time: 8
doc: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
skill: kustomize
weight: 7
---
Base Kustomize : `~/ckad/m5-04/base`. Crée l'overlay `~/ckad/m5-04/overlay` qui déploie dans
`m5-04`, préfixe les noms par `prd-`, fixe **3 réplicas**, ajoute le label
`tier=prod`, et remplace l'image par `nginx:1.28-alpine`. Applique-le.
