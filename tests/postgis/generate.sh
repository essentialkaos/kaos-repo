#!/bin/bash

declare -A versions=(
  ["10"]="3.0.9 3.1.9 3.2.5"
  ["11"]="3.0.9 3.1.9 3.2.5 3.3.4"
  ["12"]="3.0.9 3.1.9 3.2.5 3.3.4 3.4.0"
  ["13"]="3.1.9 3.2.5 3.3.4 3.4.0"
  ["14"]="3.1.9 3.2.5 3.3.4 3.4.0"
  ["15"]="3.1.9 3.2.5 3.3.4 3.4.0"
  ["16"]="3.4.0"
)

main() {
  local pg

  for pg in ${!versions[@]} ; do
    generate "$pg"
  done
}

generate() {
  local pg="$1"
  local template major_version short_version output

  echo -e "Generating recipes for PostgreSQL $pg…\n"

  for pstg in ${versions[$pg]} ; do
    major_version=${pstg:0:3}
    short_version=${major_version//./}
    template="postgis${short_version}.template"
    output="postgis${short_version}_${pg}.recipe"

    if [[ ! -f "$template" ]] ; then
      echo "✖  $output: No template for PostGIS $major_version ($short_version)"
      continue
    fi

    cat "$template" > "$output"
    sed -i "s/%PG_VERSION%/$pg/g" "$output"
    sed -i "s/%SHORT_VERSION%/$short_version/g" "$output"
    sed -i "s/%MAJOR_VERSION%/$major_version/g" "$output"
    sed -i "s/%FULL_VERSION%/$pstg/g" "$output"

    echo "✔  $output ($major_version)"
  done

  echo ""
}

main "$@"
