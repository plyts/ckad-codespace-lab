# Préparation de m2-05 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

V="v$RANDOM"
k run ingestor --image=busybox:1.37 --env="V=$V" -- sh -c 'for i in $(seq 1 30); do echo "DEBUG $i"; [ $i = 17 ] && echo "ERROR BATCH=$V"; done; sleep 3600'
