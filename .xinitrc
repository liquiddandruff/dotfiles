# load .Xresources
xrdb -merge ~/.Xresources

# urxvt daemon
urxvtd -q -f -o &

# autotune power settings
powertop --auto-tune

# start awesome and log stdout and stderr
exec awesome >> ~/.cache/awesome/stdout 2>> ~/.cache/awesome/stderr
