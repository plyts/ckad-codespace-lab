---
title: Le labo
color: gris
---
# 0 · Le labo

## Ce qui tourne dans ton Codespace

```text
Codespace (conteneur Debian, Docker-in-Docker)
├── kind : cluster ckad-a  ─ 1 control-plane + 2 workers ─ Kubernetes v1.37
│          └── Traefik (Ingress), metrics-server, kindnet (CNI + NetworkPolicy)
├── kind : cluster ckad-b  ─ 1 nœud (lab up b) : s'entraîner à changer de contexte
├── bin/ : lab, ex, mock, site
└── ~/ckad/<id>/ : tes fichiers réponse
```

Pourquoi kind : un fichier de configuration par cluster, une commande pour en recréer un propre
(`lab reset`), plusieurs clusters et contextes comme à l'examen, et une version de Kubernetes
choisie par l'image de nœud.

{{capture:lab-status}}

## Les deux configurations

| Configuration | Pour quoi faire |
|---|---|
| `CKAD lab` | Travailler : VS Code, terminal, guide sur le port 8000 |
| `CKAD exam` | S'entraîner chronométré : bureau Linux distant (port 6080), un terminal et Firefox, sans extension |

:::examen
À l'examen, chaque tâche commence par un `ssh <hôte>` vers une machine où `kubectl`, l'alias `k`,
la complétion bash, `yq`, `curl` et `wget` sont déjà prêts. Dans le labo, `lab ssh ckad-a` ouvre
un shell qui ne connaît que ce cluster. Tape `exit` pour revenir, comme à l'examen.
:::

## Contextes : le premier réflexe

{{capture:contexts}}

```bash
kubectl config use-context ckad-a
```

:::piege Le mauvais contexte
L'erreur la plus coûteuse à l'examen : faire une tâche juste… sur le mauvais cluster. Le contrôle
ne trouve rien et la tâche vaut 0. `ex check` te prévient quand ton contexte courant n'est pas
celui de l'exercice.
:::

## Le shell, réglé comme à l'examen

Le `postCreate` ajoute à `~/.bashrc` :

```bash
alias k=kubectl
source <(kubectl completion bash)
complete -o default -F __start_kubectl k
export do="--dry-run=client -o yaml"     # k run web --image=nginx $do > web.yaml
export now="--force --grace-period 0"    # k delete pod web $now
```

et à `~/.vimrc` : `set expandtab tabstop=2 shiftwidth=2 autoindent`. Dans vim, la touche Inser
est interdite à l'examen : utilise `i`.

## Les NetworkPolicy sont-elles vraiment appliquées ?

Un CNI qui ignore les NetworkPolicy laisse tout passer, et un exercice réseau semble réussi alors
qu'il ne prouve rien. `lab up` lance donc ce test réel : un Pod joint nginx, puis une règle
`deny-all` doit couper le trafic.

{{capture:netpol-test}}

Si le test échoue sur ton cluster, les contrôles de trafic bloqué s'affichent en **SKIP** (gris),
jamais en faux PASS.

## Commandes du labo

| Commande | Effet |
|---|---|
| `lab up [a\|b\|all]` | Crée le ou les clusters, précharge les images, installe Traefik et metrics-server, teste les NetworkPolicy |
| `lab reset a` | Détruit et recrée `ckad-a` (environ 3 minutes) |
| `lab status` | Versions, clusters, nœuds |
| `bash scripts/doctor.sh` | Vérifie l'absence d'IA, les versions et les clusters |

## Ton premier Pod, tout de suite

```bash
ex start d1-01
```

Tape ta réponse, puis lance `ex check d1-01`. Si quelque chose manque, le script dit quoi et pourquoi :

{{capture:check-fail}}

Une fois le Pod créé :

{{capture:check-pass}}
