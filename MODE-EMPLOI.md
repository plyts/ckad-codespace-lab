# Mode d'emploi : le labo CKAD dans Codespaces et sur GitHub Pages

Ce document s'adresse à toute personne qui veut **utiliser** ce dépôt pour préparer le CKAD,
et à celle qui le **maintient**. Il ne suppose aucune connaissance de Kubernetes ; il suppose
un compte GitHub.

- Dépôt : <https://github.com/plyts/ckad-codespace-lab>
- Guide en ligne (GitHub Pages) : <https://plyts.github.io/ckad-codespace-lab/>

---

## 1. Ce que tu obtiens

| Élément | Où | Commande |
|---|---|---|
| 2 clusters Kubernetes v1.37 (version de l'examen) | dans ton Codespace | `lab up`, `lab status` |
| 45 exercices, 9 par domaine du CKAD | `exercises/` | `ex start`, `ex check` |
| Fil conducteur (4 journées) et pannes | `scenarios/` | `ex scenario` |
| 5 examens blancs notés | `mock-exams/` | `mock start N`, `mock grade N` |
| Réponses, cachées jusqu'à ce que tu les demandes | `.answers/` | `ex solution` |
| Guide HTML bilingue : notions, journal des erreurs, cheatsheet | `docs/`, en ligne sur Pages | `site serve` |
| Cours complet, commandes exécutées | `course/course.py` → pages « Cours » du guide | `python3 scripts/verify-course.py` |
| QCU de plus de cent questions | `quiz/quiz.py` → page « QCU » du guide | `ex quiz` |

Le labo ne contient **aucune IA**. Les corrections et les explications sont écrites d'avance,
et les scripts vérifient l'état réel du cluster.

## 2. Avant de commencer : quota et coût

Codespaces est gratuit dans la limite d'un quota mensuel : **120 cœurs-heures et 15 Go-mois**
avec un compte GitHub Free, 180 cœurs-heures et 20 Go-mois avec Pro.

| Machine | Heures par mois (compte Free) | Pour quoi |
|---|---|---|
| 2 cœurs, 8 Go | environ 60 h | exercices, un cluster (`ckad-a`) |
| 4 cœurs, 16 Go | environ 30 h | examens blancs 2 à 5 (deux clusters), plus confortable |

Pour économiser le quota :

- **arrête** le Codespace quand tu as fini (menu Codespaces → *Stop codespace*) ; il s'arrête
  seul après 30 minutes d'inactivité par défaut ;
- supprime les Codespaces dont tu n'as plus besoin (<https://github.com/codespaces>) : un
  Codespace arrêté consomme encore du stockage ;
- crée `ckad-b` seulement pour les examens blancs (`lab up b`).

## 3. Ta propre copie du dépôt

Deux possibilités :

- **Recommandé : un fork.** Bouton **Fork** en haut du dépôt, puis travaille dans
  `github.com/<toi>/ckad-codespace-lab`. Tes Codespaces, ton GitHub Pages et tes notes sont à
  toi.
- **Sans fork** : ouvre un Codespace directement sur `plyts/ckad-codespace-lab`. Ça marche (le
  Codespace est facturé sur ton quota), mais tu ne pourras pas pousser de modifications.

> Sur un fork, GitHub désactive les Actions par défaut. Onglet **Actions** du fork → bouton
> *I understand my workflows, go ahead and enable them*. Sans cela, ni le selftest ni GitHub
> Pages ne tournent.

## 4. Ouvrir ton labo dans Codespaces

1. Sur la page du dépôt : **Code → Codespaces → `…` → New with options**.
2. Choisis :
   - **Branch** : `main` ;
   - **Dev container configuration** : `CKAD lab` (pour travailler) ou `CKAD exam` (pour un
     examen blanc dans un bureau Linux) ;
   - **Machine type** : 2 cœurs pour les exercices, 4 cœurs pour les examens blancs.
3. **Create codespace**, puis attends la fin de la préparation (5 à 10 minutes la première
   fois). Elle installe kind, kubectl, Helm et yq aux versions de `versions.env`, crée le
   cluster `ckad-a`, prouve que les NetworkPolicy sont appliquées et lance le contrôle
   `doctor`.
4. Dans le terminal, vérifie :

```bash
bash scripts/doctor.sh
```

Tout doit être **PASS** (des WARN sur `ckad-b` absent sont normaux). Sinon, voir la section 10.

## 5. Ta première séance (20 minutes)

```bash
ex list
```

```bash
ex start d1-01
```

La consigne s'affiche, avec le contexte (`kubectl config use-context ckad-a`) et le
namespace. Tape ta réponse dans le terminal, puis :

```bash
ex check d1-01
```

Pour chaque contrôle en échec, tu vois **attendu**, **trouvé**, **pourquoi**, la commande de
**diagnostic** et le lien vers la **doc**. Corrige, relance `ex check`. Si tu bloques :

```bash
ex hint d1-01
```

Les indices vont du plus général (1) au plus précis (3). La solution se déverrouille après trois
`ex check` ratés (`ex solution d1-01`), ou tout de suite avec `--force`.

### La règle de convergence

1. Ton **premier** `ex check` donne le **score à la sonnerie** : il est enregistré et ne change
   plus. C'est la mesure honnête de ta préparation.
2. Tu fais converger : corriger, relancer, jusqu'au vert.
3. L'exercice revient à **J+2** et **J+7** : `ex next` te les propose en premier.
4. Un exercice n'est **MAÎTRISÉ** que réussi sans indice ni solution, et une compétence n'est
   **VALIDÉE EN CONDITIONS D'EXAMEN** qu'après un examen blanc réussi à la sonnerie.

```bash
ex status
```

affiche ton tableau de progression par domaine.

## 6. Les commandes du labo

| Commande | Rôle |
|---|---|
| `ex list [1-5\|debutant\|…]` | Liste des exercices et leur statut |
| `ex start <id>` · `ex check <id>` | Démarrer (remet à zéro) · vérifier |
| `ex hint <id> [1-3]` · `ex solution <id>` | Indices · réponse de référence commentée |
| `ex reset <id>` | Remettre un exercice à zéro |
| `ex status` · `ex next` | Tableau de progression · prochain exercice conseillé |
| `ex scenario list` · `ex scenario s3-jour3` | Fil conducteur et pannes |
| `ex quiz [0-6] [-n N]` | QCU dans le terminal ; domaine 0 (bases) à 6 (scénarios, examen) |
| `ex ask <id>` | Prépare `~/ckad-questions/<id>-….md` (consigne, état du cluster, erreurs) que **tu** colles dans une IA, hors du labo |
| `mock start N` · `mock show N` · `mock time N` | Lancer un examen blanc · relire le sujet · temps restant |
| `mock grade N` · `mock review N` · `mock solution N T` | Noter · revoir les échecs · solution d'une tâche |
| `lab up [a\|b\|all]` · `lab reset a` · `lab status` | Clusters |
| `lab ssh ckad-a` | Shell limité à un cluster, comme le `ssh <hôte>` de l'examen |
| `lab wake` | Après une mise en veille : relance nœuds, DNS (CoreDNS) et Ingress |
| `site serve` | Guide HTML sur le port 8000 |

Tes fichiers réponse vont dans `~/ckad/<id>/`. Tes notes, dans `notes/<id>.md`.

## 7. Les examens blancs, en conditions d'examen

1. Crée (ou rouvre) un Codespace avec la configuration **`CKAD exam`**, machine 4 cœurs.
2. Dans le terminal : `lab up b` (le second cluster), puis `mock start 1`.
3. Onglet **Ports** → port **6080** → icône du globe : un bureau Linux s'ouvre dans le
   navigateur (mot de passe : `vscode`). Clic droit sur le bureau pour son menu ; le terminal
   `xfce4-terminal` et le navigateur `firefox-esr` sont installés (tu peux les lancer depuis un
   terminal du menu). *Ce bureau n'a pas pu être testé pendant la construction du labo : si
   un détail diffère, `doctor.sh` et ce paragraphe sont à ajuster.*
4. Travaille **uniquement** dans ce bureau : terminal, `vim` ou `nano`, et Firefox sur
   kubernetes.io/docs et helm.sh/docs. Copier-coller dans le terminal : Ctrl+Maj+C /
   Ctrl+Maj+V, comme à l'examen.
5. À la sonnerie (`mock time N`) : `mock grade N`. Le score est figé ; fais ensuite converger
   chaque tâche avec `mock review N`.

| Examen | Durée | Tâches | Quand |
|---|---|---|---|
| 1 | 60 min | 6 | après les domaines 1 et 2 |
| 2 | 90 min | 9 | après le domaine 4 |
| 3 | 120 min | 13 | après le domaine 5 |
| 4 et 5 | 120 min | 16 | conditions officielles, la dernière semaine |

## 8. Le guide HTML

### Dans ton Codespace

```bash
site serve
```

Puis onglet **Ports** → port **8000** → icône du globe. Le guide se reconstruit à chaque
`site serve`.

### En ligne, sur GitHub Pages

Le guide du dépôt d'origine : <https://plyts.github.io/ckad-codespace-lab/>

Pour publier **ton** guide (sur ton fork) :

1. **Settings → Pages → Build and deployment → Source : GitHub Actions** ;
2. pousse un commit sur `main`, ou onglet **Actions → guide → Run workflow** ;
3. le workflow `guide` recrée deux clusters sur un runner GitHub, **rejoue toutes les
   captures** de terminal, construit le site et le publie à l'adresse
   `https://<ton-compte>.github.io/ckad-codespace-lab/` (affichée dans le job `deploy`).

GitHub Pages est gratuit pour un dépôt **public** ; pour un dépôt privé, il faut GitHub Pro.

## 9. Ta progression, d'un Codespace à l'autre

Ta progression est dans `.progress/progress.json`, à l'intérieur du Codespace (ce fichier
n'est pas versionné).

- Arrêter puis redémarrer le Codespace : tout est conservé (clusters compris, réveillés par
  `lab wake` au démarrage).
- *Rebuild container* : la progression est conservée (elle est dans le dossier du dépôt),
  mais les clusters sont recréés (`lab up a`).
- **Supprimer** le Codespace : la progression est perdue. Avant, télécharge
  `.progress/progress.json` (clic droit dans l'explorateur → *Download*) et remets-le au même
  endroit dans le nouveau Codespace.

## 10. Dépannage

| Symptôme | Cause probable | Que faire |
|---|---|---|
| `cluster ckad-a injoignable. Lance : lab up a` | cluster pas créé ou supprimé | `lab up a` |
| Après une pause, `bad address`, Pods `Unknown`, Ingress muet | Docker redémarré : DNS et Traefik pas encore revenus | `lab wake` |
| Tout semble juste mais `ex check` ne trouve rien | mauvais contexte ou namespace | `kubectl config current-context` ; `ex check` le signale |
| `ImagePullBackOff` sur une image du labo | limite de débit Docker Hub | `lab images a` (recharge les images, avec repli sur le miroir) |
| Contrôles gris **SKIP** sur le réseau | ce cluster n'applique pas les NetworkPolicy | `lab netpol-test ckad-a` ; dans Codespaces, elles doivent l'être |
| `kubectl top` : `Metrics API not available` | metrics-server démarre (une minute) | attendre ; `doctor.sh` dit s'il est installé |
| Cluster dans un état incompréhensible | — | `lab reset a` (environ 3 minutes) |
| `doctor.sh` : FAIL « agents d'IA installés » | une extension ou un CLI d'IA est présent | le désinstaller ; voir la section 11 |
| Le guide affiche « NON CAPTURÉ » | captures absentes | `site capture` puis `site serve` |

## 11. Un labo sans IA

- Aucune extension d'IA n'est recommandée ; `chat.disableAIFeatures` coupe le chat et les
  suggestions de VS Code dans ce dépôt.
- Coupe Copilot dans ton compte : <https://github.com/settings/copilot>.
- `bash scripts/doctor.sh` vérifie l'absence de fichiers d'agent (CLAUDE.md, AGENTS.md…),
  d'extensions, de CLI (claude, codex, gemini…) et de clés d'API d'IA.
- Si tu veux l'avis d'une IA sur un exercice : `ex ask <id>` prépare un fichier, et c'est
  **toi** qui le colles ailleurs.

## 12. Pour le mainteneur

### Une unité (exercice, scénario ou tâche d'examen)

```text
exercises/04-config-security/d4-02/
├── task.md      front matter (id, title, domain, level, context, namespace, time, doc, skill…) + consigne
├── setup.sh     préparation (facultatif) ; reçoit CTX, NS, OUT, ROOT
├── check.sh     contrôles, avec l'API de lib/check.sh (ck_eq, ck_match, ck_true, ck_http,
│                ck_http_blocked, ck_tcp, ck_tcp_blocked)
└── hints.md     ## Indice 1 … ## Indice 3, du général au précis
.answers/d4-02/solution.sh   la réponse de référence, commentée, avec ses variantes
```

Un contrôle vérifie l'**état** du cluster, jamais la méthode. Pour chaque échec, il dit
l'attendu, le trouvé, le pourquoi, la commande de diagnostic et la doc.

### La règle d'or : le selftest

```bash
ex selftest d4-02
```

Le selftest prépare l'unité, vérifie que le contrôle **échoue**, applique la solution, puis
vérifie qu'il **passe**. GitHub Actions rejoue toutes les unités à chaque push et pull request
(workflow `selftest`), sur un runner où les NetworkPolicy et metrics-server fonctionnent.

### Changer de version de Kubernetes

1. Lis la version de l'examen dans la FAQ (lien dans `versions.md`).
2. Mets à jour `K8S_VERSION`, `KUBECTL_VERSION` et `K8S_NODE_IMAGE` (avec son digest) dans
   `versions.env`.
3. `lab reset all && ex selftest --all`, puis pousse : les deux workflows doivent être verts.
