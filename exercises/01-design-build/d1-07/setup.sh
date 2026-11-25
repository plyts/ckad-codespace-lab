# Préparation de d1-07 (CTX, NS, OUT fournis par le lanceur)
docker rmi -f ckad/hello:v1 >/dev/null 2>&1 || true
mkdir -p "$OUT"
echo 'hello CKAD' > "$OUT/index.html"
cat > "$OUT/Dockerfile" <<'EOF'
FROM busybox:1.37
COPY index.html /www/index.html
CMD ["httpd", "-f", "-p", "8080", "-h", "/www"]
EOF
