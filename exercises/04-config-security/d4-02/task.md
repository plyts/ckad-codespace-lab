---
id: d4-02
title: Secret dans une variable
domain: 4
level: debutant
context: ckad-a
namespace: d4-02
time: 4
doc: https://kubernetes.io/docs/concepts/configuration/secret/
skill: secrets
---
Dans le namespace `d4-02` :

1. Crée le Secret générique `db-cred` avec `username=admin` et `password=S3cr3t!`.
2. Crée le Pod `db-client` (image `busybox:1.37`, `sh -c 'sleep 3600'`) avec la variable
   `DB_PASSWORD` qui vaut la clé `password` du Secret.
