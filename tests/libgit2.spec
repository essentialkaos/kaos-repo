# Bibop recipe for libgit2
# See more: https://github.com/essentialkaos/bibop

pkg libgit2 libgit2-devel

fast-finish yes

command "-" "Check shared libs"
  lib-loaded libgit2.so.28

command "-" "Check headers"
  lib-header git2

command "-" "Check pkg-config"
  lib-config libgit2
