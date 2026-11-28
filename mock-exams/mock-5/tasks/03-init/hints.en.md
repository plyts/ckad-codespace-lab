## Hint 1

One `emptyDir` volume, two different mount points.

## Hint 2

Init command: `sh -c "echo 'tout va bien' > /seed/index.html"`.

## Hint 3

Test: a busybox Pod + `wget -qO- http://<IP>`.

