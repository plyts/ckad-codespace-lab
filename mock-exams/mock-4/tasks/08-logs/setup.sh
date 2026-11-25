# Préparation de m4-08 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

V="v$RANDOM"
k run sync --image=busybox:1.37 --env="V=$V" -- sh -c 'for i in $(seq 1 30); do echo "DEBUG $i"; [ $i = 17 ] && echo "ERROR SYNC=$V"; done; sleep 3600'
