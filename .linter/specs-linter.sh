#! /bin/bash

########################################################################################

# Main func
main() {
  downloadPerfecto
  printLintersInfo

  for spec in $(find . -name '*.spec' | sort) ; do
    ./perfecto --format tiny --lint-config "$1" "$spec"
  done
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
