---
id: d2-09
title: Type examen : overlay Kustomize
domain: 2
level: examen
context: ckad-a
namespace: d2-09
time: 8
doc: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
skill: kustomize
---
*Tâche type examen — 8 minutes.* Contexte `ckad-a`.

Une base Kustomize est fournie dans `~/ckad/d2-09/base`. Crée l'overlay
`~/ckad/d2-09/overlays/prod/kustomization.yaml` qui :

- utilise la base
- déploie dans le namespace `d2-09`
- préfixe les noms par `prod-`
- fixe le Deployment à **3 réplicas**
- ajoute le label `env=prod` à toutes les ressources

Applique l'overlay avec `kubectl`.
