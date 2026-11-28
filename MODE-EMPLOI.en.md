# User guide: the CKAD lab in Codespaces and on GitHub Pages

This document is for anyone who wants to **use** this repository to prepare for the CKAD, and for
whoever **maintains** it. It assumes no Kubernetes knowledge; it assumes a GitHub account.

- Repository: <https://github.com/plyts/ckad-codespace-lab>
- Online guide (GitHub Pages): <https://plyts.github.io/ckad-codespace-lab/> (English:
  <https://plyts.github.io/ckad-codespace-lab/en/>)

---

## 1. What you get

| Item | Where | Command |
|---|---|---|
| 2 Kubernetes v1.37 clusters (the exam version) | in your Codespace | `lab up`, `lab status` |
| 45 exercises, 9 per CKAD domain | `exercises/` | `ex start`, `ex check` |
| Running story (4 days) and outages | `scenarios/` | `ex scenario` |
| 5 graded mock exams | `mock-exams/` | `mock start N`, `mock grade N` |
| Answers, hidden until you ask for them | `.answers/` | `ex solution` |
| Bilingual HTML guide: concepts, error log, cheatsheet | `docs/`, online on Pages | `site serve` |
| Full course, commands actually run | `course/course.py` → "Course" pages of the guide | `python3 scripts/verify-course.py` |
| Single-answer quiz, more than a hundred questions | `quiz/quiz.py` → "Quiz" page of the guide | `ex quiz` |

The lab contains **no AI**. Corrections and explanations are written in advance, and the scripts
check the real state of the cluster.

## 2. Language: English or French

Everything exists in both languages: instructions, hints, check messages, solutions, mock exams,
course, quiz and guide.

```bash
ex lang en
```

The choice is stored in `.progress/lang` and applies to `ex`, `mock`, `lab` and `doctor.sh`.
`ex lang fr` switches back to French. For one command only: `CKAD_LANG=en ex check d1-01`. On the
HTML guide, use the **FR / EN** switch in the header.

## 3. Before you start: quota and cost

Codespaces is free within a monthly quota: **120 core-hours and 15 GB-months** with a GitHub Free
account, 180 core-hours and 20 GB-months with Pro.

| Machine | Hours per month (Free account) | For |
|---|---|---|
| 2 cores, 8 GB | about 60 h | exercises, one cluster (`ckad-a`) |
| 4 cores, 16 GB | about 30 h | mock exams 2 to 5 (two clusters), more comfortable |

To save quota:

- **stop** the Codespace when you are done (Codespaces menu → *Stop codespace*); by default it
  stops by itself after 30 minutes of inactivity;
- delete the Codespaces you no longer need (<https://github.com/codespaces>): a stopped Codespace
  still uses storage;
- create `ckad-b` only for the mock exams (`lab up b`).

## 4. Your own copy of the repository

Two options:

- **Recommended: a fork.** **Fork** button at the top of the repository, then work in
  `github.com/<you>/ckad-codespace-lab`. Your Codespaces, your GitHub Pages and your notes are
  yours.
- **Without a fork**: open a Codespace directly on `plyts/ckad-codespace-lab`. It works (the
  Codespace is billed to your quota), but you cannot push changes.

> On a fork, GitHub disables Actions by default. **Actions** tab of the fork → button *I
> understand my workflows, go ahead and enable them*. Without it, neither the selftest nor GitHub
> Pages run.

## 5. Open your lab in Codespaces

1. On the repository page: **Code → Codespaces → `…` → New with options**.
2. Choose:
   - **Branch**: `main`;
   - **Dev container configuration**: `CKAD lab` (to work) or `CKAD exam` (for a mock exam in a
     Linux desktop);
   - **Machine type**: 2 cores for the exercises, 4 cores for the mock exams.
3. **Create codespace**, then wait for the setup to finish (5 to 10 minutes the first time). It
   installs kind, kubectl, Helm and yq at the versions of `versions.env`, creates the `ckad-a`
   cluster, proves that NetworkPolicies are enforced and runs the `doctor` check.
4. In the terminal, switch to English if you want, then check:

```bash
ex lang en
```

```bash
bash scripts/doctor.sh
```

Everything must be **PASS** (WARN lines about a missing `ckad-b` are normal). Otherwise, see
section 11.

## 6. Your first session (20 minutes)

```bash
ex list
```

```bash
ex start d1-01
```

The instructions appear, with the context (`kubectl config use-context ckad-a`) and the
namespace. Type your answer in the terminal, then:

```bash
ex check d1-01
```

For every failed check you see **expected**, **found**, **why**, the **diagnostic** command and
the link to the **doc**. Fix, run `ex check` again. If you are stuck:

```bash
ex hint d1-01
```

Hints go from the most general (1) to the most precise (3). The solution unlocks after three
failed `ex check` runs (`ex solution d1-01`), or right away with `--force`.

### The convergence rule

1. Your **first** `ex check` gives the **score at the bell**: it is recorded and never changes.
   It is the honest measure of your preparation.
2. You converge: fix, run again, until green.
3. The exercise comes back at **D+2** and **D+7**: `ex next` offers them first.
4. An exercise is **MASTERED** only when passed without hint or solution, and a skill is
   **VALIDATED IN EXAM CONDITIONS** only after a mock exam passed at the bell.

```bash
ex status
```

shows your progress board by domain.

## 7. The lab commands

| Command | Role |
|---|---|
| `ex lang en\|fr` | Language of the whole lab |
| `ex list [1-5\|debutant\|…]` | List of exercises and their status |
| `ex start <id>` · `ex check <id>` | Start (resets) · check |
| `ex hint <id> [1-3]` · `ex solution <id>` | Hints · commented reference answer |
| `ex reset <id>` | Reset an exercise |
| `ex status` · `ex next` | Progress board · next recommended exercise |
| `ex scenario list` · `ex scenario s3-jour3` | Running story and outages |
| `ex quiz [0-6] [-n N]` | Quiz in the terminal; domain 0 (basics) to 6 (scenarios, exam) |
| `ex ask <id>` | Prepares `~/ckad-questions/<id>-….md` (task, cluster state, errors) that **you** paste into an AI, outside the lab |
| `mock start N` · `mock show N` · `mock time N` | Start a mock exam · read the tasks again · time left |
| `mock grade N` · `mock review N` · `mock solution N T` | Grade · review failures · solution of a task |
| `lab up [a\|b\|all]` · `lab reset a` · `lab status` | Clusters |
| `lab ssh ckad-a` | Shell limited to one cluster, like the exam's `ssh <host>` |
| `lab wake` | After a sleep: restarts nodes, DNS (CoreDNS) and Ingress |
| `site serve` | HTML guide on port 8000 |

Your answer files go into `~/ckad/<id>/`. Your notes, into `notes/<id>.md`.

## 8. Mock exams, in exam conditions

1. Create (or reopen) a Codespace with the **`CKAD exam`** configuration, 4-core machine.
2. In the terminal: `lab up b` (the second cluster), then `mock start 1`.
3. **Ports** tab → port **6080** → globe icon: a Linux desktop opens in the browser (password:
   `vscode`). Right-click on the desktop for its menu; the `xfce4-terminal` terminal and the
   `firefox-esr` browser are installed (you can start them from a terminal in the menu). *This
   desktop could not be tested while the lab was built: if a detail differs, `doctor.sh` and
   this paragraph need adjusting.*
4. Work **only** in that desktop: terminal, `vim` or `nano`, and Firefox on kubernetes.io/docs
   and helm.sh/docs. Copy-paste in the terminal: Ctrl+Shift+C / Ctrl+Shift+V, as in the exam.
5. At the bell (`mock time N`): `mock grade N`. The score is frozen; then converge every task with
   `mock review N`.

| Exam | Duration | Tasks | When |
|---|---|---|---|
| 1 | 60 min | 6 | after domains 1 and 2 |
| 2 | 90 min | 9 | after domain 4 |
| 3 | 120 min | 13 | after domain 5 |
| 4 and 5 | 120 min | 16 | official conditions, the last week |

## 9. The HTML guide

### In your Codespace

```bash
site serve
```

Then **Ports** tab → port **8000** → globe icon. The guide is rebuilt at every `site serve`; the
English version is under `/en/`.

### Online, on GitHub Pages

The guide of the original repository: <https://plyts.github.io/ckad-codespace-lab/en/>

To publish **your** guide (on your fork):

1. **Settings → Pages → Build and deployment → Source: GitHub Actions**;
2. push a commit to `main`, or **Actions → guide → Run workflow**;
3. the `guide` workflow creates two clusters on a GitHub runner, **replays every terminal
   capture**, builds the site and publishes it at `https://<your-account>.github.io/ckad-codespace-lab/`
   (shown in the `deploy` job).

GitHub Pages is free for a **public** repository; a private repository needs GitHub Pro.

## 10. Your progress, from one Codespace to another

Your progress is in `.progress/progress.json`, inside the Codespace (this file is not versioned).

- Stopping then restarting the Codespace: everything is kept (clusters included, woken up by
  `lab wake` at start).
- *Rebuild container*: progress is kept (it is in the repository folder), but the clusters are
  recreated (`lab up a`).
- **Deleting** the Codespace: progress is lost. Before that, download `.progress/progress.json`
  (right-click in the explorer → *Download*) and put it back in the same place in the new
  Codespace.

## 11. Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| `cluster ckad-a unreachable. Run: lab up a` | cluster not created or deleted | `lab up a` |
| After a pause, `bad address`, Pods `Unknown`, silent Ingress | Docker restarted: DNS and Traefik not back yet | `lab wake` |
| Everything looks right but `ex check` finds nothing | wrong context or namespace | `kubectl config current-context`; `ex check` reports it |
| `ImagePullBackOff` on a lab image | Docker Hub rate limit | `lab images a` (reloads the images, with mirror fallback) |
| Grey **SKIP** checks on networking | this cluster does not enforce NetworkPolicies | `lab netpol-test ckad-a`; in Codespaces they must be enforced |
| `kubectl top`: `Metrics API not available` | metrics-server is starting (one minute) | wait; `doctor.sh` says whether it is installed |
| Cluster in an incomprehensible state | — | `lab reset a` (about 3 minutes) |
| `doctor.sh`: FAIL "AI agents installed" | an AI extension or CLI is present | uninstall it; see section 12 |
| The guide shows "NOT CAPTURED" | captures missing | `site capture` then `site serve` |
| Messages still in French | language not set | `ex lang en` |

## 12. A lab without AI

- No AI extension is recommended; `chat.disableAIFeatures` turns off VS Code chat and suggestions
  in this repository.
- Turn off Copilot in your account: <https://github.com/settings/copilot>.
- `bash scripts/doctor.sh` checks there are no agent files (CLAUDE.md, AGENTS.md…), extensions,
  CLIs (claude, codex, gemini…) or AI API keys.
- If you want an AI's opinion on an exercise: `ex ask <id>` prepares a file, and **you** paste it
  elsewhere.

## 13. For the maintainer

### A unit (exercise, scenario or exam task)

```text
exercises/04-config-security/d4-02/
├── task.md       front matter (id, title, domain, level, context, namespace, time, doc, skill…) + instructions (French)
├── task.en.md    title + instructions in English          (generated by i18n/apply_en.py)
├── setup.sh      preparation (optional); receives CTX, NS, OUT, ROOT
├── check.sh      checks, with the lib/check.sh API (ck_eq, ck_match, ck_true, ck_http,
│                 ck_http_blocked, ck_tcp, ck_tcp_blocked)
├── check.en.txt  one line per check, in runtime order: title|||why   (generated)
├── hints.md      ## Indice 1 … ## Indice 3, from general to precise
└── hints.en.md   ## Hint 1 … ## Hint 3                     (generated)
.answers/d4-02/solution.sh      the reference answer, commented, with its variants
.answers/d4-02/solution.en.sh   same commands, English comments (generated)
```

A check verifies the **state** of the cluster, never the method. For every failure it gives the
expected value, the found value, the why, the diagnostic command and the doc.

### English content

The English text lives in `i18n/en_units.py` (exercises, scenarios), `i18n/en_mocks.py` (mock
exams) and `i18n/en_solutions.py` (solution comments). After any change to a task, a check or a
solution:

```bash
python3 i18n/apply_en.py
```

It refuses any unit without a translation, any check count that differs from `check.sh`, and any
untranslated French comment. CI runs `python3 i18n/apply_en.py --check`.

### The golden rule: the selftest

```bash
ex selftest d4-02
```

The selftest prepares the unit, checks that the check **fails**, applies the solution, then
checks that it **passes**. GitHub Actions replays every unit on each push and pull request
(`selftest` workflow), on a runner where NetworkPolicies and metrics-server work.
`CKAD_LANG=en ex selftest --all` does the same with the English solutions.

### Changing the Kubernetes version

1. Read the exam version in the FAQ (link in `versions.md`).
2. Update `K8S_VERSION`, `KUBECTL_VERSION` and `K8S_NODE_IMAGE` (with its digest) in
   `versions.env`.
3. `lab reset all && ex selftest --all`, then push: both workflows must be green.
