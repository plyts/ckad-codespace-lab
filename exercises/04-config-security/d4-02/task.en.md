---
id: d4-02
title: Secret in a variable
---
In namespace `d4-02`:

1. Create the generic Secret `db-cred` with `username=admin` and `password=S3cr3t!`.
2. Create Pod `db-client` (image `busybox:1.37`, `sh -c 'sleep 3600'`) with variable `DB_PASSWORD`
   set from the Secret's `password` key.
