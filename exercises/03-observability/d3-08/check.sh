# Contrôles de d3-08 (sourcé après lib/check.sh)
ck_true "Nom du Pod le plus gourmand" 'n=$(kn top pods --no-headers 2>/dev/null | sort -k2 -n -r | head -1 | cut -d" " -f1); [ -n "$n" ] && [ "$n" = "$(tr -d "[:space:]" < $OUT/top.txt)" ]' \
  "kubectl top pods --sort-by=cpu classe les Pods par consommation." "kubectl -n $NS top pods --sort-by=cpu; cat $OUT/top.txt"
