# Labo CKAD « de zéro à héros » — vérifié par l'exécution

Un labo d'entraînement au **CKAD** (Certified Kubernetes Application Developer) qui tourne dans
GitHub Codespaces, **sans aucune IA**. Les clusters, les scripts de vérification et tes réponses
vivent dans le même conteneur que ton terminal. Les explications et les corrections sont écrites
d'avance dans le dépôt.

- Kubernetes **v1.37**, la version de l'examen, sur des clusters [kind](https://kind.sigs.k8s.io/)
  (voir [versions.md](versions.md))
- **45 exercices**, 9 par domaine officiel, avec indices, réponses cachées et contrôles de l'état réel
- Le fil conducteur et des pannes simulées (`ex scenario`), **5 examens blancs** notés par scripts (`mock`)
- Un guide HTML (notions, scénarios, examens corrigés, commandes), sur le port 8000 ou GitHub Pages

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
| `ex start <id>` | Remet l'exercice à zéro et affiche la consigne (contexte, namespace, temps) |
| `ex check <id>` | Contrôle l'état **réel** du cluster. Pour chaque échec : attendu, trouvé, pourquoi, diagnostic, doc |
| `ex hint <id> [1-3]` | Indices progressifs |
| `ex solution <id>` | Réponse de référence commentée, après 3 essais ratés (ou `--force`) |
| `ex status` | Tableau de progression par domaine, révisions dues |
| `ex next` | Prochain exercice conseillé (révisions J+2 et J+7 d'abord) |
| `ex scenario [list\|<id>]` | Fil conducteur (application sur 4 journées) et pannes |
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
lib/check.sh     API de vérification (ck_eq, ck_match, ck_true, ck_http, ck_http_blocked)
exercises/       45 exercices : task.md, setup.sh, check.sh, hints.md
scenarios/       fil conducteur et pannes
mock-exams/      5 examens blancs
.answers/        réponses de référence (masquées dans VS Code)
app/             application fil conducteur et chart Helm local
docs/ → site/    guide HTML
scripts/         doctor.sh
notes/           tes notes (notes/<id>.md, ignorées par git)
```

## Ce qui n'a pas été exécuté pendant la construction

Le conteneur de construction n'était pas un Codespace. Tout le reste a été exécuté sur un vrai
cluster kind v1.37 ; ces points ne l'ont pas été :

- **NON TESTÉ dans Codespaces** : la création des Codespaces `lab` et `exam` elles-mêmes
  (features devcontainer, bureau noVNC, Firefox). Les scripts qu'elles lancent l'ont été.
- **Trafic NetworkPolicy** : le noyau du conteneur de construction ne prenait pas en charge les
  règles nftables de kindnet. Les contrôles de trafic bloqué sont donc passés en SKIP au selftest
  local ; GitHub Actions les exécute réellement.
- **metrics-server / `kubectl top`** : registre d'images inaccessible depuis le conteneur de
  construction, exercice `d3-08` en SKIP localement ; vérifié par GitHub Actions.
