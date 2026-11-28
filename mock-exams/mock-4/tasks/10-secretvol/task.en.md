---
id: m4-10
title: Secret as a volume
---
In namespace `m4-10`, create Secret `smtp-creds` from two literals `user=app` and `pass=Zx9-k2`, then
mount it **as a volume**, read-only, on `/etc/creds` in the existing Deployment `mailer`.
