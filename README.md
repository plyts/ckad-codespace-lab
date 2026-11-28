# Labo CKAD « de zéro à héros » — vérifié par l'exécution

> **English** — A CKAD training lab for GitHub Codespaces, **with no AI**: two Kubernetes v1.37 kind
> clusters, 45 exercises, 6 scenarios, 5 graded mock exams, a full course and a 100+ question quiz,
> all checked against the real cluster state. Everything exists in English: run `ex lang en` in the
> terminal, and read [MODE-EMPLOI.en.md](MODE-EMPLOI.en.md) and the English guide
> <https://plyts.github.io/ckad-codespace-lab/en/>.

Un labo d'entraînement au **CKAD** (Certified Kubernetes Application Developer) qui tourne dans
GitHub Codespaces, **sans aucune IA**. Les clusters, les scripts de vérification et tes réponses
vivent dans le même conteneur que ton terminal. Les explications et les corrections sont écrites
d'avance dans le dépôt.

- Kubernetes **v1.37**, la version de l'examen, sur des clusters [kind](https://kind.sigs.k8s.io/)
  (voir [versions.md](versions.md))
- **45 exercices**, 9 par domaine officiel, avec indices, réponses cachées et contrôles de l'état réel
- Le fil conducteur et des pannes simulées (`ex scenario`), **5 examens blancs** notés par scripts (`mock`)
- Un guide HTML bilingue (français / anglais) : notions, **cours complet** aux commandes exécutées,
  **QCU** de plus de cent questions, scénarios, examens corrigés, commandes ; port 8000 ou GitHub Pages

> **Mode d'emploi complet** (Codespaces, examens blancs, GitHub Pages, quotas, dépannage,
> maintenance) : [MODE-EMPLOI.md](MODE-EMPLOI.md). Guide en ligne :
> <https://plyts.github.io/ckad-codespace-lab/>

**Langue** : tout le labo (consignes, indices, contrôles, solutions, examens, cours, QCU, guide)
existe en français et en anglais. `ex lang en` passe en anglais, `ex lang fr` revient au français ;
sur le guide, sélecteur **FR / EN** dans l'en-tête.

## Démarrer

1. **Code → Codespaces → `…` → New with options**, puis choisis la configuration :
   - `CKAD lab` : VS Code et terminal, pour travailler ;
   - `CKAD exam` : un bureau Linux distant (port 6080, mot de passe `vscode`) avec un terminal et
     Firefox, comme à l'examen.
2. Attends la fin du `postCreate` (environ 5 minutes) : outils installés, cluster `ckad-a` créé,
   NetworkPolicy testées, `doctor.sh` lancé.
3. Dans le terminal :

```bash
ex list
```

```bash
ex start d1-01
```

## S'entraîner

| Commande | Rôle |
|---|---|
| `ex lang fr\|en` | Langue de tout le labo (enregistrée dans `.progress/lang`) |
| `ex start <id>` | Remet l'exercice à zéro et affiche la consigne (contexte, namespace, temps) |
| `ex check <id>` | Contrôle l'état **réel** du cluster. Pour chaque échec : attendu, trouvé, pourquoi, diagnostic, doc |
| `ex hint <id> [1-3]` | Indices progressifs |
| `ex solution <id>` | Réponse de référence commentée, après 3 essais ratés (ou `--force`) |
| `ex status` | Tableau de progression par domaine, révisions dues |
| `ex next` | Prochain exercice conseillé (révisions J+2 et J+7 d'abord) |
| `ex scenario [list\|<id>]` | Fil conducteur (application sur 4 journées) et pannes |
| `ex quiz [0-6] [-n N]` | QCU dans le terminal (mêmes questions que le guide) |
| `ex ask <id>` | Prépare `~/ckad-questions/<id>-….md` (consigne, état, erreurs) à coller **toi-même** dans une IA, hors du labo |
| `mock start N` · `mock time N` · `mock grade N` · `mock review N` · `mock solution N T` | Examens blancs 1 à 5 |
| `lab up [a\|b\|all]` · `lab reset` · `lab status` · `lab ssh ckad-a` | Clusters (`lab ssh` imite le `ssh <hôte>` de l'examen) |

### Règle de convergence

1. Le score de ton **premier** `ex check` (ou `mock grade`) est le **score à la sonnerie** : il
   est enregistré et ne change plus. C'est lui qui mesure ta préparation.
2. Pour chaque contrôle en échec, tu lis l'attendu, le trouvé et l'explication, tu corriges et
   tu relances `ex check`.
3. Après trois essais ratés, `ex solution` révèle la réponse cachée. Tu l'appliques toi-même.
4. Quand tout est au vert, l'exercice est **convergé** et revient à J+2 et J+7.
5. Une notion n'est **MAÎTRISÉE** qu'après un exercice réussi sans aide, et **VALIDÉE EN
   CONDITIONS D'EXAMEN** qu'après un examen blanc. Jamais parce que tu as lu la solution.

Les contrôles vérifient l'**état** du cluster, pas la méthode : toute autre réponse valide passe.

## Comment c'est garanti

`ex selftest` rejoue chaque réponse de référence : le contrôle doit **échouer avant** la
solution et **passer après**. GitHub Actions le relance à chaque push
([workflow](.github/workflows/selftest.yml)). Si un contrôle est faux, on corrige le contrôle,
jamais la réponse de l'apprenant.

`bash scripts/doctor.sh` vérifie qu'il n'y a ni fichier d'agent, ni extension, ni CLI, ni clé
d'API d'IA, que les outils sont aux versions figées et que les clusters tournent en v1.37.

## Retirer l'agent de construction

Le dépôt a été construit une fois par un agent (Claude Code) dans un Codespace de construction.
Ensuite :

1. supprime le Codespace de construction et la clé d'API si tu en as créé une ;
2. coupe Copilot dans ton compte GitHub (Settings → Copilot) ;
3. ouvre un **nouveau** Codespace `CKAD lab` et lance `bash scripts/doctor.sh` : tout doit être
   PASS dans la section « Aucune IA ».

## Arborescence

```text
.devcontainer/   configurations lab et exam, installation des outils
versions.env     versions figées (source unique) · versions.md : sources et faits vérifiés
kind/            clusters ckad-a (1 control-plane + 2 workers) et ckad-b (1 nœud)
infra/           Traefik (Ingress) et metrics-server
bin/             lab, ex, mock, site
lib/check.sh     API de vérification (ck_eq, ck_match, ck_true, ck_http, ck_http_blocked, ck_tcp…)
exercises/       45 exercices : task.md, setup.sh, check.sh, hints.md (+ task.en.md, hints.en.md, check.en.txt)
scenarios/       fil conducteur et pannes
mock-exams/      5 examens blancs
.answers/        réponses de référence (masquées dans VS Code)
app/             application fil conducteur et chart Helm local
course/          cours complet (47 notions, FR/EN) · quiz/ : QCU (FR/EN)
i18n/            textes anglais des unités ; apply_en.py génère les fichiers .en
docs/ → site/    guide HTML (site/ en français, site/en/ en anglais)
scripts/         doctor.sh, build_site.py, verify-course.py, verify-quiz.py
notes/           tes notes (notes/<id>.md, ignorées par git)
```

## Le guide HTML

```bash
site serve
```

Le guide est construit depuis `docs/` et sert sur le port 8000 (onglet **Ports** du Codespace).
Toutes ses sorties de terminal sont des captures réelles, que `site capture` rejoue sur
`ckad-a`. Pour le publier sur GitHub Pages : **Settings → Pages → Source : GitHub Actions**, puis
un push sur `main`. Le workflow [guide](.github/workflows/guide.yml) recrée les clusters, rejoue
les captures et déploie le site. Pages est gratuit pour un dépôt public ; un dépôt privé demande
GitHub Pro.

## Ce qui a été exécuté, où

| Vérification | Conteneur de construction | GitHub Actions (ubuntu-24.04) |
|---|---|---|
| 45 exercices, 6 scénarios, 60 tâches d'examen : échec avant, succès après la solution | oui | oui, à chaque push et pull request |
| Trafic bloqué par NetworkPolicy | non (SKIP : le noyau ne gérait pas les règles nftables de kindnet) | **oui** (`netpol@ckad-a=1`, `netpol@ckad-b=1`) |
| metrics-server / `kubectl top` (d3-08) | non (SKIP : registre d'images inaccessible) | **oui** |
| Captures du guide et du journal des erreurs | oui | oui ; ce sont les captures du runner qui sont commitées |

**NON TESTÉ** : la création des Codespaces `lab` et `exam` elles-mêmes (features devcontainer,
bureau noVNC, Firefox), faute de Codespace pendant la construction. Les scripts qu'elles lancent
(`install-tools.sh`, `shell-setup.sh`, `lab up`, `doctor.sh`) ont été exécutés. Au premier
lancement, si quelque chose casse, `bash scripts/doctor.sh` dit quoi.
