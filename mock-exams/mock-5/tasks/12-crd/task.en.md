---
id: m5-12
title: CRD
---
A CRD of group `data.m5.lab` is installed. In namespace `m5-12`, create an object `Pipeline` named `nightly-etl`
with `spec.source: s3-bucket`. Write the list of the group's resources
(`kubectl api-resources --api-group=data.m5.lab`) into `~/ckad/m5-12/resources.txt`.
