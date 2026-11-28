---
id: d3-06
title: Pending Pod: read the events
---
In namespace `d3-06`, Pod `big` stays `Pending`.

1. Write into `~/ckad/d3-06/reason.txt` the **reason** (`Reason` field) of the event that explains
   it.
2. Get Pod `big` running (same name, same image) with a request of `50m` CPU.
