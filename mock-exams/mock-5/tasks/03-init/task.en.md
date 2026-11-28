---
id: m5-03
title: Init container
---
In namespace `m5-03`, create Pod `status`: an init container `seed` (`busybox:1.37`) writes `tout va bien`
into `/seed/index.html`; container `web` (`nginx:1.27-alpine`) serves that file (same `emptyDir`
volume mounted on `/usr/share/nginx/html`).
