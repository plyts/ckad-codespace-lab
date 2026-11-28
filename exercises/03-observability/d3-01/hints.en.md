## Hint 1

`kubectl -n d3-01 logs talker` prints the container output.

## Hint 2

`grep SECRET_CODE` then `cut -d= -f2`.

## Hint 3

`kubectl -n d3-01 logs talker | grep SECRET_CODE | cut -d= -f2 > ~/ckad/d3-01/code.txt`

