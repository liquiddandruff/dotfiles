""----------------- START Vundle plugin manager setup
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
" Better statusbar
"Plugin 'bling/vim-airline'
" Tag Bar
Plugin 'majutsushi/tagbar'
" Easytags
Plugin 'xolox/vim-easytags'
" Vim-misc plugin for Easytags
Plugin 'xolox/vim-misc'
" Syntax checker
Plugin 'scrooloose/syntastic'
" Nerdtree
Plugin 'scrooloose/nerdtree'
" Nerd commenter
Plugin 'scrooloose/nerdcommenter'
" Git wrapper
Plugin 'tpope/vim-fugitive'
" Useful shortcut keys
Plugin 'tpope/vim-unimpaired'
Plugin 'tpope/vim-surround'
" Multiple cursors
Plugin 'terryma/vim-multiple-cursors'
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
colorscheme 256-grayvim
colorscheme molokai
"hi SignColumn ctermbg=235
"--------- END color schemes

set noshowmode
"let g:airline_powerline_fonts = 1
"if !exists('g:airline_symbols')
  "let g:airline_symbols = {}
"endif
"let g:airline_symbols.space = "\ua0"

"set guifont=Terminess\ Powerline\ 10
"set guifont=Liberation\ Mono\ for\ Powerline\ 10 

"if !exists('g:airline_symbols')
"	let g:airline_symbols = {}
"endif

"" unicode symbols
"let g:airline_left_sep = '»'
"let g:airline_left_sep = '▶'
"let g:airline_right_sep = '«'
"let g:airline_right_sep = '◀'
"let g:airline_symbols.linenr = '␊'
"let g:airline_symbols.linenr = '␤'
"let g:airline_symbols.linenr = '¶'
"let g:airline_symbols.branch = '⎇'
"let g:airline_symbols.paste = 'ρ'
"let g:airline_symbols.paste = 'Þ'
"let g:airline_symbols.paste = '∥'
"let g:airline_symbols.whitespace = 'Ξ'
 
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

"--------- START tagbar/easytag setup
"let g:easytags_suppress_ctags_warning=1
"let g:easytags_cmd='~/dotfiles/ctags-5.8/ctags'
"let g:tagbar_ctags_bin='~/dotfiles/ctags-5.8/ctags'
let g:tagbar_compact=1
let g:tagbar_width=30
"--------- END tagbar/easytag setup
 
"--------- Plugin Mappings
nnoremap <F5> :GundoToggle<CR>
nnoremap <F6> :NERDTreeToggle<CR>
nnoremap <CR> :TagbarToggle<CR>
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
set display+=lastline
set statusline=%02n:%<%f\ %h%m%r%=%-14.(%l,%c%V%)\ %P
" more natural splits
set splitbelow
set splitright
" save marks for up to 100 files, global marks as well
set viminfo='100,f1


" create folder structor
if !isdirectory(expand('~/.vim/undo/', 1))
	silent call mkdir(expand('~/.vim/undo', 1), 'p')
endif
if !isdirectory(expand('~/.vim/backup/', 1))
	silent call mkdir(expand('~/.vim/backup', 1), 'p')
endif
if !isdirectory(expand('~/.vim/swap/', 1))
	silent call mkdir(expand('~/.vim/swap', 1), 'p')
endif
" enable persistent undo
 if has('persistent_undo')
	 set undodir=~/.vim/undo//
	 set undofile
	 set undolevels=1000
	 set undoreload=10000
 endif
 " set backup dir
 set backup
 set writebackup
 set backupdir=~/.vim/backup//
 " set swap dir
 set directory=~/.vim/swap//

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
