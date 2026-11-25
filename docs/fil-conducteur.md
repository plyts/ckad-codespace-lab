---
title: Fil conducteur
color: gris
---
# Fil conducteur : la boutique sur quatre journées

Une petite application réaliste évolue de journée en journée et traverse les cinq domaines :

```text
 navigateur ──▶ Ingress (Traefik) ──▶ front (nginx :80)
                                        │
                                        ▼
                                      api (http-echo :5678, Service :80)
                                        │
                                        ▼
                                      redis (:6379)
```

| Journée | Ce qui change | Domaines |
|---|---|---|
| 1 | Déployer la v1 : 3 Deployments, 3 Services | 1, 2, 5 |
| 2 | ConfigMap montée, Secret en variable, ressources, 3 réplicas | 4, 2 |
| 3 | v2 défectueuse, **CrashLoopBackOff** réel, diagnostic, rollback | 2, 3 |
| 4 | NetworkPolicy en couches, Ingress | 5 |
| pannes | Trois pannes à la fois ; un ServiceAccount en `Forbidden` | 3, 4, 5 |

Chaque journée est **indépendante** : `ex scenario s3-jour3` rejoue d'abord l'état de référence
de la journée 2 (`app/boutique/jour2.yaml`), puis provoque l'incident.

## L'état de la journée 1, tel qu'il tourne

{{capture:get-all}}

## Les scénarios

{{scenarios}}

:::verif
Après chaque journée, `ex check <id>` contrôle l'état réel. Le scénario 4 vérifie aussi que le
front **ne peut pas** joindre Redis : un Pod `app=front` jetable tente la connexion, qui doit
échouer.
:::
