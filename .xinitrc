# load .Xresources
xrdb -merge ~/.Xresources

# urxvt daemon
urxvtd -q -f -o &

# start awesome and log stdout and stderr
exec awesome >> ~/.cache/awesome/stdout 2>> ~/.cache/awesome/stderr
