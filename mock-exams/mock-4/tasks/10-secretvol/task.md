---
id: m4-10
title: Secret en volume
domain: 4
level: examen
context: ckad-a
namespace: m4-10
time: 8
doc: https://kubernetes.io/docs/concepts/configuration/secret/
skill: secrets
weight: 7
---
Dans le namespace `m4-10`, crée le Secret `smtp-creds` à partir de deux littéraux
`user=app` et `pass=Zx9-k2`, puis monte-le **en volume**, en lecture seule, sur
`/etc/creds` dans le Deployment `mailer` existant.
