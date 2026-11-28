---
id: d1-09
title: Exam-style: report Pod
---
*Exam-style task — 8 minutes.* Context `ckad-a`, namespace `d1-09`.

Create a Pod `report`:

- an `emptyDir` volume named `work`, **in memory** (`medium: Memory`), limited to `16Mi`
- an init container `stamp` (`busybox:1.37`) writing `rapport du jour` into `/work/report.txt`
- a container `reader` (`busybox:1.37`) running `sh -c 'cat /work/report.txt && sleep 3600'`
- both containers mount `work` on `/work`

Save the manifest you used into `~/ckad/d1-09/report.yaml`.
