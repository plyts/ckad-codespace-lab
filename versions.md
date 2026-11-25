# Versions figées et faits vérifiés

Source unique des versions : [`versions.env`](versions.env). Tous les scripts (Codespaces, `lab`,
GitHub Actions) le lisent. Vérifié le **25 novembre 2026**.

| Composant | Version | Pourquoi |
|---|---|---|
| Kubernetes (nœuds kind) | `v1.37.0` (`kindest/node:v1.37.0@sha256:a1ed56cf…`) | Version de l'environnement d'examen CKAD (FAQ Linux Foundation) |
| kubectl | `v1.37.0` | Même version mineure que le cluster |
| kind | `v0.33.0` | Dernière release ; son image par défaut est `v1.37.0` |
| Helm | `v3.19.0` | Helm est au curriculum (« Use the Helm package manager ») |
| yq | `v4.50.1` | Préinstallé sur les hôtes d'examen |
| Traefik (Ingress) | `v3.7.20` | Contrôleur Ingress maintenu (voir plus bas) |
| metrics-server | `v0.8.0` | `kubectl top` |
| CNI | kindnet (intégré à kind) | Applique les NetworkPolicy (kube-network-policies) |

## Faits d'examen vérifiés (sources officielles)

| Fait | Ce que dit la source | Source |
|---|---|---|
| Version de Kubernetes | « The CKAD exam environment is currently running Kubernetes v1.37 », alignée sur la dernière mineure 4 à 8 semaines après sa sortie | [FAQ CKA/CKAD/CKS](https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks) |
| Durée, score | 2 heures ; 66 % pour réussir le CKAD | FAQ |
| Format | 15 à 20 tâches pratiques en ligne de commande, surveillées à distance | [Important Instructions: CKA and CKAD](https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad) |
| Hôtes | Chaque tâche se fait sur un hôte désigné : `ssh <hôte>`, puis `exit` pour revenir à `base`. `sudo -i` possible | Important Instructions |
| Outils sur les hôtes | `kubectl` avec l'alias `k` et la complétion bash, `yq`, `curl`, `wget`, `man` | Important Instructions |
| Terminal | Copier `Ctrl+Maj+C`, coller `Ctrl+Maj+V` ; touche Inser interdite (utiliser `i` dans vim) | Important Instructions |
| Documentation autorisée | kubernetes.io/docs (recherche comprise, sans ouvrir de résultat externe), kubernetes.io/blog, helm.sh/docs ; la doc Gateway API est réservée au **CKA** | [Resources Allowed](https://docs.linuxfoundation.org/tc-docs/certification/certification-resources-allowed) |
| Simulateur | Killer.sh, 2 sessions de 36 h par inscription (pas avec les inscriptions « SINGLE ») | FAQ |

Domaines et pondérations du CKAD (CNCF) : Application Design and Build 20 %, Application
Deployment 20 %, Application Observability and Maintenance 15 %, Application Environment,
Configuration and Security 25 %, Services and Networking 20 %.

**À revérifier toi-même** : le fichier détaillé des compétences du dépôt
[cncf/curriculum](https://github.com/cncf/curriculum) n'était pas accessible depuis
l'environnement de construction. Les intitulés de compétences repris dans les exercices viennent
de la version du curriculum connue de l'agent de construction. Compare-les au PDF officiel.

## Choix techniques vérifiés par l'exécution

- **Ingress : Traefik, pas ingress-nginx.** Le projet ingress-nginx est en retraite depuis
  mars 2026 (plus de release ni de correctif de sécurité). Traefik est maintenu, gère la
  ressource `Ingress` standard (`ingressClassName: traefik`), et ses manifestes sont écrits à la
  main dans [`infra/traefik.yaml`](infra/traefik.yaml). Gateway API n'est pas installé : sa
  documentation n'est autorisée qu'au CKA.
- **NetworkPolicy.** `lab up` lance `lab netpol-test` : un Pod joint nginx, puis une règle
  `deny-all` doit couper le trafic. Le résultat réel est écrit dans `.progress/caps`. Si les
  règles ne sont pas appliquées, les contrôles de trafic des exercices passent en **SKIP**
  (gris), jamais en faux PASS.
- **Chargement des images.** `kind load docker-image` échoue avec le magasin d'images containerd
  de Docker ≥ 29 (`content digest … not found`) : `lab` importe lui-même la plateforme locale
  dans chaque nœud. Les images viennent de Docker Hub, ou du miroir `mirror.gcr.io` en cas de
  limite de débit (429).
- **Hôtes restreints.** Kubernetes ≥ 1.35 refuse cgroup v1 par défaut et runc échoue sans
  `CAP_SYS_RESOURCE`. Codespaces n'a besoin d'aucun correctif ; sur un hôte ancien, `lab` ajoute
  `failCgroupV1: false` et `restrict_oom_score_adj` et l'affiche en WARN.

## Mettre à jour les versions

1. Lis la version d'examen dans la FAQ ci-dessus.
2. Change `K8S_VERSION`, `KUBECTL_VERSION` et `K8S_NODE_IMAGE` (avec son digest, depuis les notes
   de version de kind) dans `versions.env`.
3. `lab reset all && ex selftest --all` : tout doit rester vert.
