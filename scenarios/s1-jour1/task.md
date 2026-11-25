---
id: s1-jour1
title: Boutique, journée 1 : déployer la v1
domain: 0
level: intermediaire
context: ckad-a
namespace: boutique-j1
time: 12
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
skill: fil-conducteur
---
**Fil conducteur, journée 1.** Contexte `ckad-a`, namespace `boutique-j1`.
Déploie la v1 de la boutique (schéma dans `app/boutique/README.md`) :

| Composant | Deployment | Image et arguments | Réplicas | Service |
|---|---|---|---|---|
| données | `redis` | `redis:7.4-alpine` | 1 | `redis`, port 6379 |
| API | `api` | `hashicorp/http-echo:1.0.0`, argument `-text=api v1` (écoute sur 5678) | 2 | `api`, port **80** vers 5678 |
| web | `front` | `nginx:1.27-alpine` | 2 | `front`, port 80 |

Chaque Deployment porte le label `app=<nom>`. Vérifie depuis un Pod que `http://api`
répond `api v1`.
