# Contrôles de d3-01 (sourcé après lib/check.sh)
ck_eq "code.txt contient le bon code" "$(jp pod talker '{.spec.containers[0].env[0].value}')" 'tr -d "[:space:]" < $OUT/code.txt' \
  "kubectl logs talker | grep SECRET_CODE, puis ne garde que la valeur (cut -d= -f2)." "kubectl -n $NS logs talker | grep SECRET"
