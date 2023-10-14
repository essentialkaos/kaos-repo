#!/bin/bash

################################################################################

extension="pg_repack"
template="${extension}.template"

################################################################################

main() {
  local pg

  for pg in 10 11 12 13 14 15 16 ; do
    generate "$pg"
  done
}

generate() {
  local pg="$1"
  local output

  output="${extension}${pg}.recipe"

  cat "$template" > "$output"
  sed -i "s/%PG_VERSION%/$pg/g" "$output"

  echo "✔  $output (PostgreSQL $pg)"
}

################################################################################

main "$@"
