# Préparation de m3-03 (CTX, NS, OUT fournis par le lanceur)
docker rmi -f ckad/m3-app:1.0 >/dev/null 2>&1 || true
mkdir -p "$OUT/app"
echo 'ok' > "$OUT/app/index.html"
printf 'FROM busybox:1.37\nCOPY index.html /www/\nCMD ["httpd", "-f", "-p", "9000", "-h", "/www"]\n' > "$OUT/app/Dockerfile"
