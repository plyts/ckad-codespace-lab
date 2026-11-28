---
id: d4-09
title: Exam-style: configured application
---
*Exam-style task — 9 minutes.* Context `ckad-a`, namespace `d4-09`.

1. ConfigMap `portal-html`, key `index.html` = `Portal OK`.
2. Secret `portal-key`, key `API_KEY` = `k-7731`.
3. ServiceAccount `portal-sa`.
4. Deployment `portal`, 2 replicas, image `nginx:1.27-alpine`, ServiceAccount `portal-sa`:
   - the ConfigMap mounted as a volume on `/usr/share/nginx/html`
   - variable `API_KEY` read from the Secret
   - requests `50m` CPU and `32Mi` memory
