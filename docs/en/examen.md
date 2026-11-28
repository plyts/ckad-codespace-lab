---
title: Exam conditions
color: gris
---
# Exam conditions

Facts verified on 25 November 2026 on the official Linux Foundation pages (links in `versions.md`).
Check them again before booking.

## The environment

| Item | What was verified |
|---|---|
| Interface | Remote Linux desktop in the PSI Secure Browser: a terminal and Firefox |
| Hosts | Each task runs on the given host: `ssh <host>`, then `exit` to return to `base` (nested ssh is not supported) |
| Tools on the hosts | `kubectl` with the `k` alias and completion, `yq`, `curl`, `wget`, `man`; `sudo -i` available |
| `base` host | **None** of these tools: never work from `base` |
| Copy-paste | Terminal: Ctrl+Shift+C / Ctrl+Shift+V; other apps: Ctrl+C / Ctrl+V |
| Keyboard | The Insert key is forbidden (in vim, use `i`) |
| Documentation | kubernetes.io/docs (search included, without opening external results), kubernetes.io/blog, helm.sh/docs, and the Quick Reference links of each task |
| Version | Kubernetes v1.37 |
| Format | 15 to 20 tasks, 2 hours, 66% to pass, one free retake |

## Exam day checklist

**The day before**: PSI system check, clear room (nothing on the desk or on the walls), original
government ID, a single screen.

**The first five minutes**:

1. Read the task header: host, context, namespace.
2. `ssh <host>` then check: `k config current-context`, `k get nodes`.
3. If you write a lot of YAML: `export do="--dry-run=client -o yaml"`.
4. Open the docs in Firefox, on the "kubectl Quick Reference" page.

## Time management

- 120 min for about 100 points: budget **roughly 1 minute per point**; a 4% task is not worth
  12 minutes.
- **First pass**: everything quick. A task stuck for more than 2 minutes beyond its budget? Note its
  number and move on.
- **Second pass**: the flagged tasks, most profitable first.
- Keep 10 minutes to check the requested files (exact path) and namespaces.
- Before **each** task: the right host, the right context, the right namespace.

:::piege Partial credit
A task is scored per check: doing part of it earns points. Three quarters of a task beats nothing.
`mock grade` scores the same way.
:::

## The lab's mock exams

| Exam | Duration | Tasks | When |
|---|---|---|---|
| `mock 1` | 60 min | 6, one cluster | after domains 1 and 2 |
| `mock 2` | 90 min | 9, two clusters | after domain 4 |
| `mock 3` | 120 min | 13 | after domain 5 |
| `mock 4` | 120 min | 16, official conditions | week 8 |
| `mock 5` | 120 min | 16, official conditions | week 8 |

Take them in the `CKAD exam` configuration (remote desktop, terminal, Firefox), without the guide
open:

```bash
mock start 4
mock time 4
mock grade 4
mock review 4
mock solution 4 7
```

The first `mock grade` freezes the **score at the bell**. Then make each task converge (review, fix,
grade) until everything is green.

## And the Killer.sh simulator?

The registration includes two Killer.sh sessions of 36 hours, with exam-like, scored questions. They
are harder than the exam. Start the first one once `mock 4` passes at the bell, the second a few days
before the exam. You cannot repeat them at will: the lab's 5 exams are there to practise before.
