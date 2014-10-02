"----------------- START Vundle plugin manager setup
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" Plugin manager
Plugin 'gmarik/vundle' 
" It completes me
Plugin 'Valloric/YouCompleteMe'
" Better marks
Plugin 'kshenoy/vim-signature'
" Tag Bar
Plugin 'majutsushi/tagbar'
" Syntax checker
Plugin 'scrooloose/syntastic'
" Nerdtree
Plugin 'scrooloose/nerdtree'
" Git wrapper
Plugin 'tpope/vim-fugitive'
" Useful shortcut keys
Plugin 'tpope/vim-unimpaired'
" Awesome undos
Plugin 'sjl/gundo.vim'
" ColorSchemes!
Plugin 'flazz/vim-colorschemes'
" Text alignment
Plugin 'Lokaltog/vim-easymotion'
Plugin 'godlygeek/tabular'
call vundle#end()
"----------------- END Vundle plugin manager setup

"--------- START color schemes
"~/.vim/bundle/vim-colorschemes/colors/molokai.vim
" dante, 256-grayvim, wombat256, Tomorrow-Night, less, molokai, hybrid, xoria256, 
"colorscheme 256-grayvim
colorscheme molokai
"hi SignColumn ctermbg=235
"--------- END color schemes

"--------- START syntastic setup
let g:syntastic_enable_signs = 1
let g:syntastic_auto_jump    = 1
let g:syntastic_stl_format   = '[%E{Err: %fe #%e}%B{, }%W{Warn: %fw #%w}]'
"--------- END syntastic setup

"--------- START ycm setup
let g:ycm_complete_in_comments = 1
let g:ycm_global_ycm_extra_conf = '~/.vim/.ycm_extra_conf.py'
"--------- END ycm setup

"--------- START easymotion setup
let g:EasyMotion_do_mapping = 0 " Disable default mappings
" Bi-directional find motion
nmap s <Plug>(easymotion-s)
let g:EasyMotion_smartcase = 0
" jump to lines below/above
map <Leader>j <Plug>(easymotion-j)
map <Leader>k <Plug>(easymotion-k)
"--------- END easymotion setup

"--------- START tagbar setup
let g:tagbar_ctags_bin='~/dotfiles/ctags-5.8/ctags'
"--------- END tagbar setup
 
"--------- Plugin Mappings
nnoremap <F5> :GundoToggle<CR>
nnoremap <F6> :NERDTreeToggle<CR>
nnoremap <F7> :TagbarToggle<CR>
nnoremap <F10> :SignatureRefresh<CR>

"----------------- END Plugins

" user interface
syntax on
set number
set title
set ignorecase
set smartcase
set hlsearch		" highlight search
set incsearch

" editor settings
" set mouse=a
set hidden			" enables edited buffer switching
set wildmenu		" vim fuzzy select
set scrolloff=2
set nowrap
set backspace=indent,eol,start
" tabs
set tabstop=4
set shiftwidth=4
" statusline
set laststatus=2 
set statusline=%02n:%<%f\ %h%m%r%=%-14.(%l,%c%V%)\ %P
" more natural splits
set splitbelow
set splitright
" save marks for up to 100 files, global marks as well
set viminfo='100,f1

" filetype autocompletion and indentation, also needed for vundle
filetype plugin indent on

" bindings
" instead of ctr-w then j, just ctr-j
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>
inoremap jk <Esc>
inoremap JK <Esc>
" ctr tab to switch buffers
nnoremap ,l :bn<CR>
nnoremap ,; :bp<CR>

" functions 
" get the diff of current buffer with original buffer (diffsaved diffoff)
function! s:DiffWithSaved()
  let filetype=&ft
  diffthis
  vnew | r # | normal! 1Gdd
  diffthis
  exe "setlocal bt=nofile bh=wipe nobl noswf ro ft=" . filetype
endfunction
com! DiffSaved call s:DiffWithSaved()
