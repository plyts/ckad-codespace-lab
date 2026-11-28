---
id: m3-02
title: Init container
---
In namespace `m3-02`, create Pod `landing`: an init container `seed` (`busybox:1.37`) writes `bienvenue m3`
into `/seed/index.html`; container `web` (`nginx:1.27-alpine`) serves that file (same `emptyDir`
volume mounted on `/usr/share/nginx/html`).
