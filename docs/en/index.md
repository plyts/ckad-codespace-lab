---
title: Home
color: gris
---
# The CKAD, from zero to hero

This guide goes with the lab in the repository. It contains **no unverified claim**: every terminal
output is a real capture (`scripts/capture-docs.sh`), every exercise is replayed by `ex selftest`,
and exam facts come from the official pages cited in
[versions.md](https://github.com/plyts/ckad-codespace-lab/blob/main/versions.md).

New here? Start with the [user guide](mode-emploi.html): opening your Codespace, your first session,
mock exams, the online guide and troubleshooting.

- **[Full course](cours.html)**: every exam topic, chapter by chapter, with commands and YAML
  **actually executed** on a v1.37 cluster (and their real outputs).
- **[Quiz](quiz.html)**: over a hundred single-choice questions on every topic and scenario, each
  answer explained with a precise command; also in the terminal with `ex quiz`.
- **Version française** : bouton **FR** en haut à droite de chaque page.

## The exam at a glance

| | |
|---|---|
| Format | 15 to 20 hands-on command-line tasks, remotely proctored |
| Duration | 2 hours |
| Passing score | 66% |
| Version | Kubernetes **v1.37** (Linux Foundation FAQ, November 2026) |
| Allowed documentation | kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs |
| Simulator | Killer.sh, 2 sessions of 36 h with the registration |

## The five domains and their colour

| Domain | Weight | Colour | Page |
|---|---|---|---|
| Application Design and Build | 20% | <span class="dot bleu"></span> blue | [1 · Design and Build](d1-design-build.html) |
| Application Deployment | 20% | <span class="dot jaune"></span> yellow | [2 · Deployment](d2-deployment.html) |
| Application Observability and Maintenance | 15% | <span class="dot vert"></span> green | [3 · Observability](d3-observability.html) |
| Application Environment, Configuration and Security | 25% | <span class="dot orange"></span> orange | [4 · Config and Security](d4-config-security.html) |
| Services and Networking | 20% | <span class="dot violet"></span> purple | [5 · Services and Networking](d5-networking.html) |

## How to train

1. **Read the topic** in the domain page or the [course](cours.html) (10 to 20 minutes, no more).
2. **Do the exercise** in the terminal: `ex start d1-01`, type your answer, then `ex check d1-01`.
3. **Converge**: every failure shows what was expected, what was found, why, and the diagnostic
   command. Fix, rerun. Hints with `ex hint`, solution after 3 tries with `ex solution`.
4. **Redo it from scratch**, timed: it comes back on its own at D+2 and D+7 (`ex next`).
5. **Mock exams** once a domain is mastered: `mock start 1` … `mock start 5`.

:::pourquoi
The score of your **first** `ex check` is frozen: it is the only honest measure of your readiness.
Reading the solution never counts as a success.
:::

## Suggested schedule (exam not booked yet)

For a beginner comfortable with Linux, Docker and Git, about **10 hours a week**:

| Week | Content | Exercises |
|---|---|---|
| 1 | [The lab](installation.html) and the [fundamentals](fondamentaux.html); first Pod | `d1-01`, `s1-jour1` |
| 2 | Domain 1 (20%) | `d1-*` |
| 3 | Domain 2 (20%) | `d2-*`, `s3-jour3` |
| 4 | Domain 3 (15%) | `d3-*`, `s5-pannes` |
| 5 | Domain 4 (25%): the biggest share, a week and a half | `d4-*`, `s2-jour2`, `s6-panne-rbac` |
| 6 | End of domain 4, domain 5 (20%) | `d5-*`, `s4-jour4` |
| 7 | Mock exams 1 to 3, targeted review (`ex status`), the quiz | `mock 1-3`, `ex quiz` |
| 8 | Mock exams 4 and 5 in official conditions, then the Killer.sh simulator | `mock 4-5` |

When `mock 4` and `mock 5` pass **at the bell** above 66%, book your exam date and start the first
Killer.sh session (harder than the exam, on purpose).
