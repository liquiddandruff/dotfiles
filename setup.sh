#!/bin/bash

# Vars
dotfile_dir="$HOME/dotfiles"
flags="-s"


# Configs
mkdir -p "$HOME/.config"
#ln $flags "${dotfile_dir}/.config/mpv" "$HOME/.config/mpv"
ln $flags "${dotfile_dir}/.mpd" "$HOME/.mpd"
ln $flags "${dotfile_dir}/.ncmpcpp" "$HOME/.ncmpcpp"


# Scripts
mkdir -p "$HOME/bin"
ln $flags "${dotfile_dir}/bin/"*.py "$HOME/bin"
ln $flags "${dotfile_dir}/bin/"*.sh "$HOME/bin"
# Drop the ".sh" from all scripts.
for script in "$HOME/bin/"*.sh; do mv "$script" "${script/'.sh'}"; done


# Dot files
# We use cp here instead of ln because cp excludes folders from linking.
# pass -s flag to create symlink
cp $flags "${dotfile_dir}"/.* "$HOME"


# Neovim
mkdir -p "$HOME/.config/nvim"
ln $flags "${dotfile_dir}/init.vim" "$HOME/.config/nvim"
# Awesome
mkdir -p "$HOME/.config/awesome"
ln $flags "${dotfile_dir}/awesome/rc.lua" "$HOME/.config/awesome/rc.lua"
ln $flags "${dotfile_dir}/awesome/powerarrow-dark-custom" "$HOME/.config/awesome/themes/powerarrow-dark-custom"
# Zathura
mkdir -p "$HOME/.config/zathura"
ln $flags "${dotfile_dir}/zathura/zathurarc" "$HOME/.config/zathura/zathurarc"
# Htop
mkdir -p "$HOME/.config/htop"
ln $flags "${dotfile_dir}/htop/htoprc" "$HOME/.config/htop/htoprc"

