" notes
"
" :r! echo %
"
" print ascii value of character under cursor
" ga
"
" print hex value of actual bytes stored in file (assumes utf-8)
" g8
"
" change lists
" g;
" g,


"let g:python_host_prog='/usr/bin/python2'
" auto install plug if not found
if empty(glob('~/.config/nvim/autoload/plug.vim'))
	silent !curl -fLo ~/.config//nvim/autoload/plug.vim --create-dirs
	\ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
	autocmd VimEnter * PlugInstall
endif

call plug#begin('~/.config/nvim/plugged')
	" Editor config
	Plug 'editorconfig/editorconfig-vim'
	" YCM
	Plug 'Valloric/YouCompleteMe'
		let g:ycm_confirm_extra_conf=0
		let g:ycm_collect_identifiers_from_tags_files=1
		nnoremap <Space>d :YcmCompleter GoTo<CR>
		nnoremap <Space>e :YcmCompleter GoToDefinition<CR>
		nnoremap <Space>w :YcmCompleter GetDoc<CR>
		nnoremap <Space>q :YcmCompleter GoToInclude<CR>
		" python only
		nnoremap <Space>r :YcmCompleter GoToReferences<CR>
		" On update...
		" Regen makefiles
		" $ cmake -G "Unix Makefiles" -DPATH_TO_LLVM_ROOT=~/ycm_temp/llvm_root_dir . ~/.config/nvim/plugged/YouCompleteMe/third_party/ycmd/cpp
		" Make it
		" $ cmake --build . --target ycm_core
	" UltiSnips engine
	Plug 'SirVer/ultisnips'
		let g:UltiSnipsExpandTrigger="<c-x>"
		let g:UltiSnipsJumpForwardTrigger="<c-b>"
		let g:UltiSnipsJumpBackwardTrigger="<c-z>"
	" UltiSnips snippets
	Plug 'honza/vim-snippets'
	" Doxygen snippets gen
	Plug 'mrtazz/DoxygenToolkit.vim'
		nnoremap <Space>j :Dox<CR>
	" Doxygen/Javadoc highlighting
	Plug 'vim-scripts/DoxyGen-Syntax'
	" Vim fzf
	Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
	Plug 'junegunn/fzf.vim'
		" Mapping selecting mappings
		nnoremap <silent> <C-p> :Files<CR>
		nnoremap <silent> <Space>p :GitFiles<CR>
		nnoremap <silent> <Space>o :Buffers<CR>
		nnoremap <silent> <Space>i :Lines<CR>
	" Smart Indents
	Plug 'tpope/vim-sleuth'
	" Autoindent
	Plug 'Chiel92/vim-autoformat'
	" Unite
	Plug 'Shougo/unite.vim'
	" HTML
	Plug 'mattn/emmet-vim'
	  " CTRL+Y+,
	" Auto close tags
	Plug 'alvan/vim-closetag'
		let g:closetag_filenames = "*.html,*.jsx,*.js"
	" Undo tree
	Plug 'sjl/gundo.vim'
		nnoremap <F5> :GundoToggle<CR>
	" Status line
	Plug 'itchyny/lightline.vim'
		let g:lightline = {
			\ 'colorscheme': 'jellybeans',
			\ 'component': {
			\   'readonly': '%{&readonly?"":""}',
			\ },
			\ 'separator': { 'left': '', 'right': '' },
			\ 'subseparator': { 'left': '', 'right': '' }
			\ }
	" Auto completion
	Plug 'Shougo/deoplete.nvim'
	" File browser
	Plug 'scrooloose/nerdtree'
		nnoremap <F6> :NERDTreeToggle<CR>
	" Ctags tagbar 
	Plug 'majutsushi/tagbar'
		nmap <Return> :TagbarToggle<CR>
	" Async lint
	Plug 'benekastah/neomake'
		let g:neomake_open_list = 1
		let g:neomake_place_signs = 1
		let g:neomake_error_sign = {
			\ 'text': 'E>',
			\ 'texthl': 'Error',
		\ }
		let g:neomake_warning_sign = {
			\ 'text': 'W>',
			\ 'texthl': 'TermCursorNC',
		\ }
	" Prose
	Plug 'junegunn/goyo.vim'
	Plug 'junegunn/limelight.vim'
		let g:limelight_conceal_ctermfg = 240
		autocmd! User GoyoEnter Limelight
		autocmd! User GoyoLeave Limelight!
	" Wiki
	Plug 'vimwiki/vimwiki'
	" Shows search results as you're typing
	Plug 'junegunn/vim-pseudocl'
	Plug 'junegunn/vim-oblique'
		let g:oblique#incsearch_highlight_all = 1
		let g:oblique#clear_highlight = 1
		"let g:oblique#prefix = "\\v" " Very Magic
	" Comment stuff out
	Plug 'tpope/vim-commentary'
	" Surround stuff
	Plug 'tpope/vim-surround'
	" Easy motion
	Plug 'Lokaltog/vim-easymotion'
		let g:EasyMotion_do_mapping = 0
		let g:EasyMotion_smartcase = 0
		" bidirectional
		nmap s <Plug>(easymotion-s)
	" Nerdtree
	Plug 'scrooloose/nerdtree'
		nnoremap <F6> :NERDTreeToggle<CR>
	" Markdown live preview
	function! BuildComposer(info)
	  if a:info.status != 'unchanged' || a:info.force
		!cargo build --release
		UpdateRemotePlugins
	  endif
	endfunction
	Plug 'euclio/vim-markdown-composer', { 'do': function('BuildComposer') }
		let g:markdown_composer_autostart = 0
	" Filetype plugins
	Plug 'sheerun/vim-polyglot'
	" Jellybean colorscheme
	Plug 'nanotech/jellybeans.vim'
call plug#end()


filetype plugin indent on


"" user interface
" neovim true colour (urxvt no support yet)
"let $NVIM_TUI_ENABLE_TRUE_COLOR = 1
colorscheme jellybeans
set title
set number
"set lazyredraw
" search
set ignorecase
set smartcase
set hlsearch
set incsearch

"" editor settings
set hidden 			" enables edited buffer switching
set wildmenu 		" fuzzy select
set scrolloff=2
set nowrap
set backspace=indent,eol,start
" invisible chars
set lcs=tab:▸\ ,trail:·,eol:¬,nbsp:_,space:␣
" tabs
set tabstop=4
set shiftwidth=4
" statusline
set laststatus=2 
set display+=lastline
set statusline=%02n:%<%f\ %h%m%r%=%-14.(%l,%c%V%)\ %P
" natural splits
set splitbelow
set splitright

" gf to correctly open files when working on js
set suffixesadd+=.js

"" mappings
" instead of ctr-w then j, just ctr-j
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>
inoremap jk <Esc>
inoremap JK <Esc>
" map F4 to toggle header/source file
map <F4> :e %:p:s,.h$,.X123X,:s,.cpp$,.h,:s,.X123X$,.cpp,<CR>
" write when not sudo
cmap w!! w !sudo tee % >/dev/null
" Terminal Splits
cmap Hterm sp <bar> terminal
cmap Vterm vsp <bar> terminal
" Maps Tab to indent blocks of text in visual mode
vmap <TAB> >gv
vmap <BS> <gv
vmap <S-TAB> <gv
" use hjkl-movement between rows when soft wrapping:
nnoremap j gj
nnoremap k gk
vnoremap j gj
vnoremap k gk
" include the default behaviour by doing reverse mappings so you can move linewise with gj and gk:
nnoremap gj j
nnoremap gk k
" easier buffer nav
nnoremap ,l :bn<Cr>
nnoremap ,; :bp<Cr>
" easier pop back from jumping to tag
nnoremap <C-[> <C-t>

" persistent undos and swap dir
set backupdir=~/.config/nvim/tmp/backups//
set undodir=~/.config/nvim/tmp/undo//
set directory=~/.config/nvim/tmp/swap//
if !isdirectory(expand(&backupdir))
	call mkdir(expand(&backupdir), "p")
endif
if !isdirectory(expand(&undodir))
	call mkdir(expand(&undodir), "p")
endif
if !isdirectory(expand(&directory))
	call mkdir(expand(&directory), "p")
endif
set undofile
set undolevels=1000
set undoreload=1000

"" misc
" Improve Neovim startup time by disabling python and host check
let g:python_host_skip_check= 1
let g:python3_host_skip_check= 1
"let g:loaded_python_provider = 1
"let g:loaded_python3_provider = 1

" use %% to expand dir of current buffer, to edit other files in same dir
cabbr <expr> %% expand('%:p:h')

"" functions

" Quick Terminal
" Spawns a terminal in a small split for quick typing of commands
" Also maps <Esc> to quit out of the terminal
function QuitTerminal()
	setlocal buflisted
	silent! bd! quickterm
endfunction
function! QuickTerminal()
	10new
	terminal
	file quickterm
endfunction
tnoremap <silent> <Esc> <C-\><C-n>:call QuitTerminal()<CR>
nnoremap <silent> <Leader>t :call QuickTerminal()<CR>

" modify selected text using combining diacritics
command! -range -nargs=0 Overline        call s:CombineSelection(<line1>, <line2>, '0305')
command! -range -nargs=0 Underline       call s:CombineSelection(<line1>, <line2>, '0332')
command! -range -nargs=0 DoubleUnderline call s:CombineSelection(<line1>, <line2>, '0333')
command! -range -nargs=0 Strikethrough   call s:CombineSelection(<line1>, <line2>, '0336')

function! s:CombineSelection(line1, line2, cp)
  execute 'let char = "\u'.a:cp.'"'
  execute a:line1.','.a:line2.'s/\%V[^[:cntrl:]]/&'.char.'/ge'
endfunction

" Open current file with another program
function! Openwith(program)
	silent! execute "!" . a:program . " " . expand('%:p') . " &"
endfunction
command! -bang -nargs=* Openwith call Openwith(<q-args>)

function! s:DiffWithSaved()
  let filetype=&ft
  diffthis
  vnew | r # | normal! 1Gdd
  diffthis
  exe "setlocal bt=nofile bh=wipe nobl noswf ro ft=" . filetype
endfunction
com! DiffSaved call s:DiffWithSaved()

" word processing mode
func! WordProcessorMode() 
  setlocal formatoptions=1 
  setlocal noexpandtab 
  map j gj 
  map k gk
  setlocal spell spelllang=en_ca
  "set thesaurus+=/Users/sbrown/.vim/thesaurus/mthesaur.txt
  set complete+=s
  "set formatprg=par
  setlocal wrap 
  setlocal linebreak 
endfu 
com! WordProcessor call WordProcessorMode()

" Append modeline after last line in buffer.
" Use substitute() instead of printf() to handle '%%s' modeline in LaTeX
" files.
function! AppendModeline()
  let l:modeline = printf(" vim: set ts=%d sw=%d tw=%d %set :",
        \ &tabstop, &shiftwidth, &textwidth, &expandtab ? '' : 'no')
  let l:modeline = substitute(&commentstring, "%s", l:modeline, "")
  call append(line("$"), l:modeline)
endfunction
nnoremap <silent> <Leader>ml :call AppendModeline()<CR>
