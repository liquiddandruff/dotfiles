# load .Xresources
xrdb -merge ~/.Xresources

# urxvt daemon
urxvtd -q -f -o &

# start awesome
exec awesome
