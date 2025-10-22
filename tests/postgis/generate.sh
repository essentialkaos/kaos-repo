#!/bin/bash

main() {
  if [[ "$#" -eq 0 ]] ; then
    echo "Usage: ./generate.sh {postgis-version}"
    exit 0
  fi

  for pg_ver in $(seq 13 18) ; do
    generate "$1" "$pg_ver"
  done
}

generate() {
  local postgis_ver="$1"
  local pg_ver="$2"

  local template major_version short_version output

  major_version=${postgis_ver:0:3}
  short_version=${major_version//./}
  template="postgis${short_version}.template"
  output="postgis${short_version}_${pg_ver}.recipe"

  echo -e -n "Generating recipe for ${postgis_ver}/${pg_ver}: "

  if [[ ! -f "$template" ]] ; then
    echo "✖ "
    echo "$output: No template for PostGIS $major_version\n"
    return 1
  fi

  cat "$template" > "$output"
  sed -i "s/%PG_VERSION%/$pg_ver/g" "$output"
  sed -i "s/%SHORT_VERSION%/$short_version/g" "$output"
  sed -i "s/%MAJOR_VERSION%/$major_version/g" "$output"
  sed -i "s/%FULL_VERSION%/$postgis_ver/g" "$output"

  echo "✔  $output"

  return 0
}

main "$@"
