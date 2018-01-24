#! /bin/bash

########################################################################################

main() {
  downloadPerfecto
  printLintersInfo

  local has_errors

  for spec in $(find . -name '*.spec' | sort) ; do
    ./perfecto --format tiny --lint-config "$1" "$spec"

    if [[ $? -ne 0 && -z "$has_errors" ]] ; then
      has_errors=true
    fi
  done

  if [[ -n "$has_errors" ]] ; then
    exit 1
  fi

  exit 0
}

downloadPerfecto() {
  wget https://apps.kaos.io/perfecto/latest/linux/x86_64/perfecto
  
  if [[ $? -ne 0 ]] ; then
    exit 1
  fi

  chmod +x perfecto
}

printLintersInfo() {
  echo -e "\n"
  rpmlint -V
  ./perfecto -v
  echo -e "\n"
}

########################################################################################

main $@
