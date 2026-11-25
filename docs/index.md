---
title: Accueil
color: gris
---
# Le CKAD, de zéro à héros

Ce guide accompagne le labo du dépôt. Il ne contient **aucune affirmation non vérifiée** : chaque
sortie de terminal est une capture réelle (`scripts/capture-docs.sh`), chaque exercice est rejoué
par `ex selftest`, et les faits d'examen viennent des pages officielles citées dans
[versions.md](https://github.com/plyts/ckad-codespace-lab/blob/main/versions.md).

## L'examen en bref

| | |
|---|---|
| Format | 15 à 20 tâches pratiques en ligne de commande, surveillées à distance |
| Durée | 2 heures |
| Score de réussite | 66 % |
| Version | Kubernetes **v1.37** (FAQ Linux Foundation, novembre 2026) |
| Documentation autorisée | kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs |
| Simulateur | Killer.sh, 2 sessions de 36 h avec l'inscription |

## Les cinq domaines et leur couleur

| Domaine | Poids | Couleur | Page |
|---|---|---|---|
| Application Design and Build | 20 % | <span class="dot bleu"></span> bleu | [1 · Design and Build](d1-design-build.html) |
| Application Deployment | 20 % | <span class="dot jaune"></span> jaune | [2 · Deployment](d2-deployment.html) |
| Application Observability and Maintenance | 15 % | <span class="dot vert"></span> vert | [3 · Observability](d3-observability.html) |
| Application Environment, Configuration and Security | 25 % | <span class="dot orange"></span> orange | [4 · Config and Security](d4-config-security.html) |
| Services and Networking | 20 % | <span class="dot violet"></span> violet | [5 · Services and Networking](d5-networking.html) |

## Comment t'entraîner

1. **Lis la notion** dans la page du domaine (10 à 20 minutes, pas plus).
2. **Fais l'exercice** dans le terminal : `ex start d1-01`, tape ta réponse, puis `ex check d1-01`.
3. **Converge** : chaque échec affiche l'attendu, le trouvé, le pourquoi et la commande de
   diagnostic. Corrige, relance. Indices avec `ex hint`, solution après 3 essais avec `ex solution`.
4. **Refais-le à blanc**, chronométré : il revient tout seul à J+2 et J+7 (`ex next`).
5. **Examens blancs** quand un domaine est maîtrisé : `mock start 1` … `mock start 5`.

:::pourquoi
Le score de ton **premier** `ex check` est figé : c'est la seule mesure honnête de ta
préparation. Relire la solution n'est jamais compté comme une réussite.
:::

## Programme proposé (examen non planifié)

Pour un débutant à l'aise avec Linux, Docker et Git, à raison d'environ **10 heures par semaine** :

| Semaine | Contenu | Exercices |
|---|---|---|
| 1 | [Le labo](installation.html) et les [fondamentaux](fondamentaux.html) ; premier Pod | `d1-01`, `s1-jour1` |
| 2 | Domaine 1 (20 %) | `d1-*` |
| 3 | Domaine 2 (20 %) | `d2-*`, `s3-jour3` |
| 4 | Domaine 3 (15 %) | `d3-*`, `s5-pannes` |
| 5 | Domaine 4 (25 %) : la plus grosse part, une semaine et demie | `d4-*`, `s2-jour2`, `s6-panne-rbac` |
| 6 | Fin du domaine 4, domaine 5 (20 %) | `d5-*`, `s4-jour4` |
| 7 | Examens blancs 1 à 3, révisions ciblées (`ex status`) | `mock 1-3` |
| 8 | Examens blancs 4 et 5 en conditions officielles, puis le simulateur Killer.sh | `mock 4-5` |

Quand `mock 4` et `mock 5` passent **à la sonnerie** au-dessus de 66 %, réserve ta date
d'examen et lance la première session Killer.sh (plus difficile que l'examen, c'est voulu).
