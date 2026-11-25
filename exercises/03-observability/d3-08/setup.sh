# Préparation de d3-08 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

pick=$((RANDOM % 3))
for i in 0 1 2; do
  if [ $i = $pick ]; then cmd='while true; do :; done'; else cmd='sleep 3600'; fi
  k run "worker-$i" --image=busybox:1.37 -- sh -c "$cmd"
done
