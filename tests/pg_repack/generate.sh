#!/bin/bash

################################################################################

extension="pg_repack"
template="${extension}.template"

################################################################################

main() {
  if [[ $# -eq 0 ]] ; then
    echo "Usage: ./generate.sh {pg_repack_version}"
  fi

  for pg in $(seq 13 17) ; do
    generate "$1" "$pg"
  done
}

generate() {
  local repack_ver="$1"
  local pg_ver="$2"

  local output

  output="${extension}${pg_ver}.recipe"

  cat "$template" > "$output"
  sed -i "s/%REPACK_VERSION%/$repack_ver/g" "$output"
  sed -i "s/%PG_VERSION%/$pg_ver/g" "$output"

  echo "✔  $output (PostgreSQL $pg_ver)"
}

################################################################################

main "$@"
