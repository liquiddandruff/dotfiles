# always use tmux
#if [[ ! $TERM =~ screen ]]; then
    #exec tmux
#fi

# Path to your oh-my-zsh installation.
export ZSH=/home/steven/.oh-my-zsh

# themes in ~/.oh-my-zsh/themes/
ZSH_THEME="agnoster"
#af-magic

HIST_STAMPS="mm/dd/yyyy"

# plugins in ~/.oh-my-zsh/plugins/
plugins=(git vi-mode)

export PATH="/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl"

source $ZSH/oh-my-zsh.sh

# virtualenv
export WORKON_HOME=$HOME/.virtualenvs
source /usr/bin/virtualenvwrapper.sh

unsetopt AUTO_CD

export PATH=$PATH:/home/steven/bin:/home/steven/Android/Sdk/platform-tools
export VISUAL="nvim"
export EDITOR="nvim"
export ANDROID_HOME=/home/steven/Android/Sdk
# zsh vi-mode editor
export VISUAL="nvim"

# edit
alias vim="nvim"
alias evimrc="vim ~/dotfiles/init.vim"
alias ewm="vim ~/dotfiles/awesome/rc.lua"
alias etmux="vim ~/dotfiles/.tmux.conf"
alias emp="vim ~/dotfiles/.ncmpcpp/config"
alias erc="nvim ~/.zshrc"
alias src="source ~/.zshrc"

# to dirs
alias torepos="cd ~/GitRepos"
alias tosat="torepos; cd SFUSat"
alias todots="cd ~/dotfiles"
alias todb="cd ~/Dropbox"
alias todl="cd ~/Downloads"

alias gl="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# execute
alias xwifi="systemctl start netctl-auto@wlp1s0"
alias xwifikill="sudo ip link set wlp1s0 down"
alias xwifiup="sudo ip link set wlp1s0 up"
alias xdb="dropbox &|"
alias mp3dl="cd $HOME/Music && youtube-dl --extract-audio -f bestaudio --audio-format mp3 --no-playlist"
alias xsd="sudo mount -t auto /dev/sdb1 /mnt/sd"
alias xusb="sudo mount /dev/sdb1 /mnt/usb"
alias xunmountsd="sync; sudo umount /mnt/sd"
alias xunmountusb="sync; sudo umount /mnt/usb"
alias xtags="ctags -R --exclude=.git .; du -sh tags"
alias xstudio="~/Downloads/android-studio/bin/studio.sh >> /dev/null 2>&1 &|"

# TI
alias xhalcogen="wine ~/ti/Hercules/HALCoGen/v04.06.00/HALCOGEN.exe"
alias xccs="~/ti/ccsv7/eclipse/ccstudio"
alias xuniflash="sudo /opt/ti/uniflash_4.1/node-webkit/nw"

# program re-aliases
# ipython in venv
alias ipy="python -c 'import IPython; IPython.terminal.ipapp.launch_new_instance()'"
# always show statusbar, scale to screen, vi keys
alias qiv="qiv -I --vikeys"

# system alias
alias wtf="ping 8.8.8.8"
# get more usb info (bus, port, etc)
alias xlsusb='sudo cat /sys/kernel/debug/usb/devices | grep -E "^([TSPD]:.*|)$"'
# sleep screen
alias xsleep="xset dpms force standby"
alias xbat="cat /sys/class/power_supply/BAT1/{status,capacity}"
# stop ghostscript from coming up when I mistype gst (git status alias)
alias gs=""
# monitor
alias xmonoff="xrandr --output LVDS1 --off --output HDMI1 --mode 1920x1080"
alias xmonon="xrandr --output LVDS1 --auto --output HDMI1 --off"
alias xhdmihrsame="xrandr --output HDMI1 --mode 1920x1080 --primary --same-as LVDS1"
alias xhdmihr="xrandr --output HDMI1 --mode 1920x1080 --left-of LVDS1"
alias xhdmilr="xrandr --output HDMI1 --mode 1680x1050 --left-of LVDS1"
alias xhdmioff="xrandr --output HDMI1 --off"


##### notes
### clipboard stuff
# CLIPBOARD output: xsel -bo 
# PRIMARY input: xsel -i 
### xclip cat image to clipboard with proper types
# cat 3.4fig3.png | xclip -selection clipboard -t image/png

### updating YCM
## navigate to ~/.config/nvim/plugged/YCM
# ./install.py --clang-completer -tern-completer
## if vim complains about not finding python3...
# sudo pip install --upgrade neovim

### get args from prev command
# $ !line :column
# $ !* all args, !:0 command name, !:2 second arg, !:$ last arg

### bluetooth excursion
# $ systemctl start bluetooth.service
# $ bluetoothctl

### netcat things
## server
# $ netcat -l -p 4444 localhost
## client
# $ netcat localhost 4444

### pa stuff
# $ pulseaudio --kill
# $ pamixer
# $ pactl
# $ pacmd
## sinks http://unix.stackexchange.com/questions/65246/change-pulseaudio-input-output-from-shell
# $ pactl list short sink-inputs
# $ pactl move-sink-input <ID> <SINK>
## reset alsa when fubar
# $ alsactl restore
#

### tar lol
## make archive
# $ tar -zcvf out.tar.gz ./dir
## extract archive
# $ tar -zxvf out.tar.gz -C ./out

### sd format
## fat32
# get disk
# $ lsblk
# partition it, enter 0xb for W95 FAT32
# $ sudo fdisk /dev/sdb
# format it
# $ sudo mkdosfs -F 32 /dev/sdb1
# use it
# $ sudo mount -t auto /dev/sdb1 /mnt/sd

# screenshot
# $ shutter
xscn() {
  import -window root /tmp/$(date '+%Y%m%d-%H%M%S').png
}
xscnw() {
  sleep 2; import root /tmp/$(date '+%Y%m%d-%H%M%S').png
}

# replace in out
replace() {
  ag -l $1 | xargs perl -pi.bak -e "s/$1/$2/g"
}

# throw away stdout and stderr, and disown
pdf() {
	zathura $1 &> /dev/null &|
}

# control print service
ccups() {
	systemctl $1 org.cups.cupsd.service
}

# tonas USER PASS
tonas() {
	smbclient //wdnas/Media $2 -U $1
}

# mountnas USER PASS
mountnas() {
	sudo mkdir /mnt/nas
	sudo mount -t cifs //wdnas/Media /mnt/nas -o user=$1,password=$2
}
# unmount nas, all, lazy
umountnas() {
	sudo umount -a -t cifs -l /mnt/nas
}

setbn() {
	sudo tee /sys/class/backlight/intel_backlight/brightness <<< $1
}
setb() {
	case $1 in
	  h|'')
	    setbn 4650;;
	  m)
	    setbn 1000;;
	  l)
	    setbn 0;;
	esac
	return
	if [[ "$1" == "h" || -z $1 ]]; then
	  setbn 4650
	elif [[ "$1" == "m" ]]; then
	  setbn 2000
	elif [[ "$1" == "l" ]]; then
	  setbn 0
	fi
}

# fast cd to school hw
tohw() {
  #PS3="Pick dir: " 
  todb;
  cd school;
  # init empty array
  dirs=()
  for DIR in `find . -mindepth 1 -maxdepth 1 -type d`; do
    dirs+=($DIR)
  done
  # if passed index and index exists in dirs, cd to it
  if [[ -n $1 && -n ${dirs[$1]} ]]; then
    cd ${dirs[$1]}
    return
  fi
  select opt in "${dirs[@]}"
  do
    # if opt is empty, ask again
    if [[ -z $opt ]]; then
      continue
    fi
    case $REPLY in
      *) 
	cd $opt
	break
	;;
    esac
  done
}

# mv gcode to sd
xgcode() {
  # init empty array
  gcodeFiles=()
  # find ~/Downloads -cnewer ~/Downloads/z_stop_upSlic3r.gcode -name "*.gcode"
  # find ~/Downloads -name "*.gcode" -exec ls -t "{}" +; 
  for gcode in `find ~/Downloads -name "*.gcode" -exec ls -t "{}" +;`; do
    gcodeFiles+=($gcode)
  done
  # if passed index and index exists in gcodeFiles, move it
  if [[ -n $1 && -n ${gcodeFiles[$1]} ]]; then
    sudo cp -v ${gcodeFiles[$1]} /mnt/sd
    return
  fi
  select opt in "${gcodeFiles[@]}"
  do
    # if opt is empty, ask again
    if [[ -z $opt ]]; then
      continue
    fi
    case $REPLY in
      *) 
	sudo cp -v $opt /mnt/sd
	break
	;;
    esac
  done
}

# trim mp4 start end
# ffmpeg -i movie.mp4 -ss 00:00:03 -t 00:00:08 -async 1 cut.mp4
# mp4 to gif
# ffmpeg -i input.mp4 -vf scale=320:-1 -r 10 -f image2pipe -vcodec ppm - | \
  # convert -delay 10 -loop 0 - output.gif

# colorize manpages
man() {
    env LESS_TERMCAP_mb=$'\E[01;31m' \
    LESS_TERMCAP_md=$'\E[01;38;5;74m' \
    LESS_TERMCAP_me=$'\E[0m' \
    LESS_TERMCAP_se=$'\E[0m' \
    LESS_TERMCAP_so=$'\E[38;5;246m' \
    LESS_TERMCAP_ue=$'\E[0m' \
    LESS_TERMCAP_us=$'\E[04;38;5;146m' \
    man "$@"
}

# fix keys
# delete key
#bindkey "^[[3~" delete-char
# home key
#bindkey "^[[7~" beginning-of-line
# end key
#bindkey "^[[8~" end-of-line

# shift up down left right arrows
#^[[5~^[[6~^[[7~^[[8~

# save path on cd
function cd {
    builtin cd $@
    pwd > ~/.last_dir
}
# restore last saved path
if [ -f ~/.last_dir ]
    then cd `cat ~/.last_dir`
fi

# end config
# --------------------------------------------------------------------------------


# Auto-completion
# ---------------
if [[ -f /usr/share/zsh/site-functions/_fzf ]]; then
  source /usr/share/zsh/site-functions/_fzf
fi

# Key bindings
# ------------
if [[ $- == *i* ]]; then

# CTRL-T - Paste the selected file path(s) into the command line
__fsel() {
  local cmd="${FZF_CTRL_T_COMMAND:-"command find -L . \\( -path '*/\\.*' -o -fstype 'dev' -o -fstype 'proc' \\) -prune \
    -o -type f -print \
    -o -type d -print \
    -o -type l -print 2> /dev/null | sed 1d | cut -b3-"}"
  eval "$cmd" | $(__fzfcmd) -m | while read item; do
    printf '%q ' "$item"
  done
  echo
}

__fzfcmd() {
  [ ${FZF_TMUX:-1} -eq 1 ] && echo "fzf-tmux -d${FZF_TMUX_HEIGHT:-40%}" || echo "fzf"
}

fzf-file-widget() {
  LBUFFER="${LBUFFER}$(__fsel)"
  zle redisplay
}
zle     -N   fzf-file-widget
bindkey '^T' fzf-file-widget

# ALT-C - cd into the selected directory
fzf-cd-widget() {
  local cmd="${FZF_ALT_C_COMMAND:-"command find -L . \\( -path '*/\\.*' -o -fstype 'dev' -o -fstype 'proc' \\) -prune \
    -o -type d -print 2> /dev/null | sed 1d | cut -b3-"}"
  cd "${$(eval "$cmd" | $(__fzfcmd) +m):-.}"
  zle reset-prompt
}
zle     -N    fzf-cd-widget
bindkey '\ec' fzf-cd-widget

# CTRL-R - Paste the selected command from history into the command line
fzf-history-widget() {
  local selected num
  selected=( $(fc -l 1 | $(__fzfcmd) +s --tac +m -n2..,.. --tiebreak=index --toggle-sort=ctrl-r -q "${LBUFFER//$/\\$}") )
  if [ -n "$selected" ]; then
    num=$selected[1]
    if [ -n "$num" ]; then
      zle vi-fetch-history -n $num
    fi
  fi
  zle redisplay
}
zle     -N   fzf-history-widget
bindkey '^R' fzf-history-widget

fi


[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
