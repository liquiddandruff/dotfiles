# start custom settings 
PATH=$PATH:~/bin
PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting
PATH=$PATH:$HOME/.rvm/gems/ruby-2.0.0-p247/gems/jekyll-1.1.2/bin # Add jekyll to PATH
PATH=$PATH:$JAVA_HOME/bin
PATH=$PATH:~/dotfiles/ctags-5.8 # for VIM ctags
PATH=$PATH:~/Desktop/android-studio-sdk/platform-tools # add adb to path
PATH=$PATH:~/GitRepos/esp-open-sdk/xtensa-lx106-elf/bin # add xtensa gcc to path
PATH=$PATH:/usr/lib/postgresql/9.3/bin # postgres to path
# arducopter
PATH=$PATH:$HOME/GitRepos/Avian/ardupilot/Tools/autotest
PATH=/usr/lib/ccache:$PATH

export ESP_HOME="/home/steven/GitRepos/esp-open-sdk"
export SMING_HOME="/home/steven/GitRepos/Sming/Sming"
export JAVA_HOME=/usr/java/jdk1.8.0_05
export EDITOR="vim"

# tmux shell completion
source ~/bin/tmux-shell-completion.sh
alias src="source ~/.bashrc"
alias erc="vim ~/.bashrc"
alias ewm="cd ~/.config/awesome/; vim rc.lua"
alias etmux="vim ~/.tmux.conf"
alias evimrc="vim ~/.vimrc"
alias ebash="tobin; vim bash"

# freq dirs
alias tostudio="cd ~/Desktop/android-studio/"
alias tovim="cd ~/dotfiles"
alias tobin="cd ~/bin"
alias todev="cd ~/dev"
alias towm="cd ~/.config/awesome"
alias todots="cd ~/dotfiles"
alias torepos="cd ~/GitRepos"
alias toschool="todb; cd school"
alias xnas="thunar smb://10.42.0.19/media"
# IdEA
alias toidea="torepos; cd IdEA"
alias tocsas="toidea; cd csa-site"
alias xcsa="tocsas; ./manage.py runserver 0.0.0.0:11000"
alias tocsaf="toidea; cd csa-firmware"
alias tonode="torepos; cd nodemcu-firmware"
alias toespsdk="cd ~/GitRepos/esp-open-sdk"
alias toespdev="toespsdk; cd source-code-examples"
alias xflashNODE="tonode; make flash"
alias xflashAT="toespsdk; cd esptool/test; ../esptool.py --port /dev/ttyUSB0 write_flash 0x00000 boot_v1.1.bin 0x01000 user1.bin 0x7c000 esp_init_data_default.bin 0x7e000 blank.bin"
alias xflashX="toespsdk; cd esptool/test; ../esptool.py --port /dev/ttyUSB0 write_flash 0x00000 blank.bin 0x01000 blank.bin 0x40000 blank.bin 0x7c000 blank.bin 0x7e000 blank.bin"
# Avian
alias toavianaw="ssh -i ~/.ssh/aviankey ubuntu@avianrobotics.com"
function scpavian {
	echo "Copying things from local $1 to remote $2";
	scp -rv -i ~/.ssh/aviankey $1 ubuntu@avianrobotics.com:$2;
}
alias toavian="torepos; cd Avian"
alias toaviansrv="toavi; cd AvianServer"
function toapi { ssh pi@$1; }
# misc
alias totest="todev; cd test"
alias tosite="cd ~/dev/liquiddandruff.github.com"
alias tositecss="cd ~/dev/liquiddandruff.github.com/assets/themes/custom/css"
alias tositeposts="cd ~/dev/liquiddandruff.github.com/_posts"
alias tositehtml="cd ~/dev/liquiddandruff.github.com/_includes/themes/custom"
alias tovps="ssh root@192.3.169.100" 
alias toram="ssh -i ~/.ssh/ram root@ansible.stevenhuang.ca"
alias toalex="ssh -i ~/.ssh/alexdo ansible@www.db.alexsepkowski.com -t 'command; bash -l'"
alias todb="cd ~/Dropbox"
alias todl="cd ~/Downloads"
alias todocs="cd ~/Documents"

# projects
alias tospeed="torepos; cd SpeedCrunch/src"

alias packagesite="rake theme:package name="custom""
alias updatesite="tobin; ./blueVPSftp; cd -"
alias _updatesite="tobin; ./lftpUpdate"

alias xzombies="ps aux | grep 'Z'"
alias xsite="tosite; jekyll -w --safe server"
alias xsitepid="lsof -wni tcp:4000"
alias xkill="kill -9\\"
alias xclient="todev; love untitledClient"
alias xserver="todev; love untitledServer"
alias xapthistory="( zcat $( ls -tr /var/log/apt/history.log*.gz ) ; cat /var/log/apt/history.log ) | egrep '^(Start-Date:|Commandline:)' | grep -v aptdaemon | egrep '^Commandline:'"

# programs
alias xsql="mysql -u root -p"
alias xstudio="tostudio; ./bin/studio.sh"
alias xstudioupdate="~/Desktop/android-studio/bin/update_studio.sh"
alias xscrn="shutter"
alias xard="todl; ./arduino-1.6.5/arduino"
alias xdb="~/.dropbox-dist/dropboxd &"
alias xesp="todl; java -jar ./ESPlorer/ESPlorer.jar"

# utilities
alias xwifimon="wavemon"
alias gettree="ncdu"
alias xtemp="sensors"
# csa, 10.10.0.1, 1234567890,
alias xap="sudo hotspotd start"
alias xwifi="nmcli nm wifi\\"
alias xbat="upower -i /org/freedesktop/UPower/devices/battery_BAT1"
alias xdv="sudo hibernate"
alias xcv='dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend'
alias xtheme="~/.config/awesome/switch-theme.sh"
alias xhdmihr="xrandr --output HDMI1 --mode 1920x1080 --left-of LVDS1"
alias xhdmilr="xrandr --output HDMI1 --mode 1680x1050 --left-of LVDS1"
alias xhdmioff="xrandr --output HDMI1 --off"
alias setb="sudo su -c \"echo 4648 >/sys/class/backlight/intel_backlight/brightness\""
function setbn { sudo su -c "echo $1 >/sys/class/backlight/intel_backlight/brightness"; }
function heylol {
	"diff \\"
}

# remaps
alias dus="du -hs * | sort -h"
alias tmux="tmux -2"
alias less="less -R" #enable color
alias pdf="evince"
alias h="history"
alias pulseaudioc="pavucontrol"
# git
alias gl="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# make ctrl+d don't exit shell
set -o ignoreeof
# history verify and expand !! etc
shopt -s histverify

# end custom settings


# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep -n --color=always'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi


# custom PS1
export PS1="\[\e[00;37m\]\u@\h:\w\[\e[0m\]\[\e[00;31m\]\\$\[\e[0m\]\[\e[00;37m\] \[\e[0m\]"
[ -f ~/.fzf.bash ] && source ~/.fzf.bash
