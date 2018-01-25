#! /bin/bash

########################################################################################

# Main func
main() {
  downloadPerfecto
  printLintersInfo

  local has_errors

  for spec in $(find . -name '*.spec' | sort) ; do
    ./perfecto -e error -f tiny -c "$1" "$spec"

    if [[ $? -ne 0 && -z "$has_errors" ]] ; then
      has_errors=true
    fi
  done

  if [[ -n "$has_errors" ]] ; then
    exit 1
  fi

  exit 0
}

# Donwload latest version of perfecto
downloadPerfecto() {
  wget https://apps.kaos.io/perfecto/latest/linux/x86_64/perfecto
  
  if [[ $? -ne 0 ]] ; then
    exit 1
  fi

  chmod +x perfecto
}

# Print info about version of rpmlint and perfecto
printLintersInfo() {
  echo -e "--------------------------------------------------------------------------------\n"
  rpmlint -V
  ./perfecto -v
  echo -e "--------------------------------------------------------------------------------\n"
}

########################################################################################

main $@
