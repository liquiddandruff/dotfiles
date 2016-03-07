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
ln $flags "${dotfile_dir}/scripts/"*.sh "$HOME/bin"
ln $flags "${dotfile_dir}/scripts/"**/*.sh "$HOME/bin"
# Drop the ".sh" from all scripts.
for script in "$HOME/bin/"*.sh; do mv "$script" "${script/'.sh'}"; done


# Dot files
# We use cp here instead of ln because cp excludes folders from linking.
# pass -s flag to create symlink
cp $flags "${dotfile_dir}"/.* "$HOME"


# Neovim
mkdir -p "$HOME/.config/nvim"
ln $flags "${dotfile_dir}/init.vim" "$HOME/.config/nvim"

