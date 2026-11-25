# Préparation de d3-01 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

CODE="ck-$RANDOM$RANDOM"
k run talker --image=busybox:1.37 --env="CODE=$CODE" -- sh -c \
  'for i in $(seq 1 60); do echo "INFO traitement $i"; [ $i = 37 ] && echo "SECRET_CODE=$CODE"; done; sleep 3600'
