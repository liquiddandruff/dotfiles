#!/bin/bash
sh fonts/install.sh
echo
dotfiles=".vim .bashrc .vimrc .tmux.conf"
dotfilesDIR=~/dotfiles
for dotfile in $dotfiles; do
	echo "Creating symlink for $dotfile"
	echo -e "\tln -s $dotfilesDIR/$dotfile ~/$dotfile"
	ln -s $dotfilesDIR/$dotfile ~/$dotfile
	echo
done
# ln -s ~/dotfiles/.tmux.conf ~/.tmux.conf

