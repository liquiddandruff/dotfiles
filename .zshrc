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

export PATH=$PATH:/home/steven/bin
export EDITOR="nvim"
# zsh vi-mode editor
export VISUAL="nvim"
alias vim="nvim"
alias evimrc="vim ~/dotfiles/init.vim"
alias ewm="vim ~/dotfiles/awesome/rc.lua"
alias erc="nvim ~/.zshrc"
alias src="source ~/.zshrc"

# to dirs
alias torepos="cd ~/GitRepos"
alias todots="cd ~/dotfiles"
alias todb="cd ~/Dropbox"
alias todl="cd ~/Downloads"
alias wtf="ping 8.8.8.8"

alias gl="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# execute
alias xwifi="systemctl start netctl-auto@wlp1s0"
alias xwifikill="sudo ip link set wlp1s0 down"
alias xdb="dropbox &|"
alias mp3dl="cd $HOME/Music && youtube-dl --extract-audio -f bestaudio --audio-format mp3 --no-playlist"

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

# fix keys
# delete key
bindkey "^[[3~" delete-char
# home key
bindkey "^[[7~" beginning-of-line
# end key
bindkey "^[[8~" end-of-line

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

