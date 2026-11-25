---
title: Conditions d'examen
color: gris
---
# Conditions d'examen

Faits vérifiés le 25 novembre 2026 sur les pages officielles de la Linux Foundation (liens dans
`versions.md`). Revérifie-les avant de réserver.

## L'environnement

| Élément | Ce qui est vérifié |
|---|---|
| Interface | Bureau Linux distant dans le PSI Secure Browser : un terminal et Firefox |
| Hôtes | Chaque tâche se fait sur l'hôte indiqué : `ssh <hôte>`, puis `exit` pour revenir à `base` (le ssh imbriqué n'est pas pris en charge) |
| Outils sur les hôtes | `kubectl` avec l'alias `k` et la complétion, `yq`, `curl`, `wget`, `man` ; `sudo -i` possible |
| Hôte `base` | **Aucun** de ces outils : ne travaille jamais depuis `base` |
| Copier-coller | Terminal : Ctrl+Maj+C / Ctrl+Maj+V ; autres applications : Ctrl+C / Ctrl+V |
| Clavier | Touche Inser interdite (dans vim, `i`) |
| Documentation | kubernetes.io/docs (recherche comprise, sans ouvrir de résultat externe), kubernetes.io/blog, helm.sh/docs, et les liens de la Quick Reference de chaque tâche |
| Version | Kubernetes v1.37 |
| Format | 15 à 20 tâches, 2 heures, 66 % pour réussir, un repassage inclus |

## Fiche jour J

**La veille** : check système PSI, pièce dégagée (rien sur le bureau ni aux murs), pièce
d'identité officielle originale, un seul écran.

**Les cinq premières minutes** :

1. Lis l'en-tête de la tâche : hôte, contexte, namespace.
2. `ssh <hôte>` puis vérifie : `k config current-context`, `k get nodes`.
3. Si tu fais beaucoup de YAML : `export do="--dry-run=client -o yaml"`.
4. Ouvre la doc dans Firefox, sur la page « kubectl Quick Reference ».

## Gestion du temps

- 120 min pour environ 100 points : compte **à peu près 1 minute par point** ; une tâche à 4 %
  ne mérite pas 12 minutes.
- **Première passe** : tout ce qui est rapide. Une tâche bloque plus de 2 minutes au-delà de
  son temps ? Note son numéro et passe.
- **Deuxième passe** : les tâches notées, de la plus rentable à la moins rentable.
- Garde 10 minutes pour vérifier les fichiers demandés (chemin exact) et les namespaces.
- Avant **chaque** tâche : le bon hôte, le bon contexte, le bon namespace.

:::piege Le crédit partiel
Une tâche est notée par vérifications : en faire une partie rapporte des points. Mieux vaut trois
quarts de tâche que rien. `mock grade` note de la même façon.
:::

## Les examens blancs du labo

| Examen | Durée | Tâches | Quand |
|---|---|---|---|
| `mock 1` | 60 min | 6, un seul cluster | après les domaines 1 et 2 |
| `mock 2` | 90 min | 9, deux clusters | après le domaine 4 |
| `mock 3` | 120 min | 13 | après le domaine 5 |
| `mock 4` | 120 min | 16, conditions officielles | semaine 8 |
| `mock 5` | 120 min | 16, conditions officielles | semaine 8 |

Lance-les dans la configuration `CKAD exam` (bureau distant, terminal, Firefox), sans le guide
ouvert :

```bash
mock start 4
mock time 4
mock grade 4
mock review 4
mock solution 4 7
```

Le premier `mock grade` fige le **score à la sonnerie**. Ensuite, fais converger chaque tâche
(review, correction, grade) jusqu'au vert.

## Et le simulateur Killer.sh ?

L'inscription inclut deux sessions Killer.sh de 36 heures, avec des questions proches de
l'examen et notées. Elles sont plus difficiles que l'examen. Lance la première quand `mock 4`
passe à la sonnerie, la seconde quelques jours avant l'examen. Tu ne peux pas la refaire à
volonté : les 5 examens du labo servent à s'entraîner avant.
