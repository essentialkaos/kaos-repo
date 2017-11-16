#! /bin/bash

########################################################################################

NORM=0
BOLD=1
UNLN=4
RED=31
GREEN=32
BROWN=33
BLUE=34
MAG=35
CYAN=36
GREY=37
DARK=90

CL_NORM="\e[${NORM}m"
CL_BOLD="\e[${BOLD}m"
CL_UNLN="\e[${UNLN}m"
CL_RED="\e[${RED}m"
CL_GREEN="\e[${GREEN}m"
CL_BROWN="\e[${BROWN}m"
CL_BLUE="\e[${BLUE}m"
CL_MAG="\e[${MAG}m"
CL_CYAN="\e[${CYAN}m"
CL_GREY="\e[${GREY}m"
CL_DARK="\e[${DARK}m"
CL_BL_RED="\e[${RED};1m"
CL_BL_GREEN="\e[${GREEN};1m"
CL_BL_BROWN="\e[${BROWN};1m"
CL_BL_BLUE="\e[${BLUE};1m"
CL_BL_MAG="\e[${MAG};1m"
CL_BL_CYAN="\e[${CYAN};1m"
CL_BL_GREY="\e[${GREY};1m"
CL_UL_RED="\e[${RED};4m"
CL_UL_GREEN="\e[${GREEN};4m"
CL_UL_BROWN="\e[${BROWN};4m"
CL_UL_BLUE="\e[${BLUE};4m"
CL_UL_MAG="\e[${MAG};4m"
CL_UL_CYAN="\e[${CYAN};4m"
CL_UL_GREY="\e[${GREY};4m"
CL_BG_RED="\e[${RED};7m"
CL_BG_GREEN="\e[${GREEN};7m"
CL_BG_BROWN="\e[${BROWN};7m"
CL_BG_BLUE="\e[${BLUE};7m"
CL_BG_MAG="\e[${MAG};7m"
CL_BG_CYAN="\e[${CYAN};7m"
CL_BG_GREY="\e[${GREY};7m"

########################################################################################

# Path to file used for caching linter output
tmp_file=""

# Path to config with rpmlint prefs
rpmlint_conf=""

# Number of files with errors or warnings
file_count=0

# Numbers of errors
errors_count=0

# Numbers of warnings
warn_count=0

########################################################################################

main() {
  tmp_file=$(mktemp)

  rpmlint -V

  if [[ -f $1 && -s $1 ]] ; then
    rpmlint_conf="$1"
  fi

  echo ""

  for spec in $(git --no-pager show --name-only --oneline --decorate HEAD | sed -e '1d' | egrep '.spec$') ; do
    runLinter "$spec"
  done

  rm -f $tmp_file

  if [[ $errors_count -ne 0 ]] ; then
    echo -e "\n${CL_RED}Found $errors_count errors and $warn_count warnings in $file_count files${CL_NORM}"
    exit 1
  elif [[ $warn_count -ne 0 ]]; then
    echo -e "\n${CL_BROWN}Found $errors_count errors and $warn_count warnings in $file_count files${CL_NORM}"
  else
    echo -e "\n${CL_GREEN}All spec files is well formated${CL_NORM}"
  fi
}

runLinter() {
  local spec="$1"
  local file=$(echo "$spec" | sed 's/\.\///g')

  if [[ -n "$rpmlint_conf" ]] ; then
    rpmlint -f $rpmlint_conf $spec 2>/dev/null > $tmp_file
  else
    rpmlint $spec 2>/dev/null > $tmp_file
  fi

  local errors=$(tail -1 $tmp_file | grep -E -o '[0-9]{1,} errors' | sed 's/ errors//')
  local warnings=$(tail -1 $tmp_file | grep -E -o '[0-9]{1,} warnings' | sed 's/ warnings//')

  if [[ -z "$errors" || -z "$warnings" ]] ; then
    echo -e "${CL_DARK}[${CL_NORM}${CL_RED}  ERROR  ${CL_NORM}${CL_DARK}]${CL_NORM} $file"
    ((file_count++))
    ((errors_count++))
    showLintResult
  fi

  if [[ $errors -eq 0 && $warnings -eq 0 ]] ; then
    printf "${CL_DARK}[${CL_NORM} ${CL_GREEN} 0${CL_NORM} ${CL_DARK}⋮${CL_NORM} ${CL_GREEN} 0${CL_NORM} ${CL_DARK}]${CL_NORM} %s\n" "$file"
  else
    if [[ $errors -eq 0 && $warnings -ne 0 ]] ; then
      printf "${CL_DARK}[${CL_NORM} ${CL_GREEN}%2s${CL_NORM} ${CL_DARK}⋮${CL_NORM} ${CL_BROWN}%2s${CL_NORM} ${CL_DARK}]${CL_NORM} %s\n" "$errors" "$warnings" "$file"
      warn_count=$(( $warn_count + $warnings ))
    elif [[ $errors -ne 0 && $warnings -eq 0 ]] ; then
      printf "${CL_DARK}[${CL_NORM} ${CL_RED}%2s${CL_NORM} ${CL_DARK}⋮${CL_NORM} ${CL_GREEN}%2s${CL_NORM} ${CL_DARK}]${CL_NORM} %s\n" "$errors" "$warnings" "$file"
      errors_count=$(( $errors_count + $errors ))
    else
      printf "${CL_DARK}[${CL_NORM} ${CL_RED}%2s${CL_NORM} ${CL_DARK}⋮${CL_NORM} ${CL_BROWN}%2s${CL_NORM} ${CL_DARK}]${CL_NORM} %s\n" "$errors" "$warnings" "$file"
      errors_count=$(( $errors_count + $errors ))
      warn_count=$(( $warn_count + $warnings ))
    fi

    ((file_count++))

    showLintResult
  fi
}

showLintResult() {
  echo -e "${CL_GREY}"
  cat $tmp_file | sed 's/^/  /g'
  echo -e "${CL_NORM}"
}

########################################################################################

main $@
