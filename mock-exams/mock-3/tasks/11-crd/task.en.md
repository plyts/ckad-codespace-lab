---
id: m3-11
title: Custom resource
---
A CRD of group `ops.m3.lab` is installed. In namespace `m3-11`, create an object `Maintenance` named `weekly`
with `spec.window: dimanche 02h`. Write the list of the group's resources
(`kubectl api-resources --api-group=ops.m3.lab`) into `~/ckad/m3-11/resources.txt`.
