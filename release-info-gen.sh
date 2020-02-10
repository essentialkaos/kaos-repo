#!/usr/bin/env bash

################################################################################

TYPE_ADD="A"
TYPE_MOD="(A|R|M)"
TYPE_DEL="D"

################################################################################

changes_cache=""

################################################################################

main() {

  git checkout -B master origin/master &>/dev/null
  git checkout develop &>/dev/null
  
  createChangesCache
  listAdditions
  listModifications
  listDeletions
  clearChangesCache

}

listAdditions() {
  local line spec_info spec spec_name app_name app_desc header_shown

  while read -r line ; do
    
    # shellcheck disable=SC2206
    spec_info=($line)
    spec="${spec_info[1]}"
    spec_name=$(basename "$spec")
    
    if isSpecMoved "$spec_name" ; then
      continue
    fi

    if [[ -z "$header_shown" ]] ; then
      echo -e "### New packages\n"
      header_shown=true
    fi

    app_name=$(getSpecValue "$spec" "name")
    app_desc=$(getSpecValue "$spec" "summary")

    echo "- \`${app_name}\` (_${app_desc}_)"

  done < <(getChanges "$TYPE_ADD")

  echo ""
}

listModifications() {
  local line spec_info spec spec_name app_name app_ver header_shown

  while read -r line ; do

    if [[ -z "$header_shown" ]] ; then
      echo -e "### Updates\n"
      header_shown=true
    fi
   
    # shellcheck disable=SC2206
    spec_info=($line)

    if [[ "${spec_info[0]:0:1}" == "R" ]] ; then
      spec="${spec_info[2]}"
    else
      spec="${spec_info[1]}"
    fi

    spec_name=$(basename "$spec")

    if [[ "${spec_info[0]}" == "A" ]] ; then
      if ! isSpecMoved "$spec_name" ; then
        continue
      fi
    fi

    app_name=$(getSpecValue "$spec" "name")
    app_ver=$(getSpecValue "$spec" "version")

    echo "- \`${app_name}\` updated to $app_ver"

  done < <(getChanges "$TYPE_MOD")

  echo ""
}

listDeletions() {
  local line spec_info spec spec_name app_name header_shown

  while read -r line ; do
   
    # shellcheck disable=SC2206
    spec_info=($line)
    spec="${spec_info[1]}"
    spec_name=$(basename "$spec")

    if isSpecMoved "$spec_name" ; then
      continue
    fi

    if [[ -z "$header_shown" ]] ; then
      echo -e "### Deletions\n"
      header_shown=true
    fi

    app_name=$(getNameFromSpec "$spec")

    echo "- \`$app_name\` removed"
  done < <(getChanges "$TYPE_DEL")

  echo ""
}

getChanges() {
  if [[ $# -eq 1 ]] ; then
    grep -E "^$1" "$changes_cache"
  else
    cat "$changes_cache"
  fi
}

isSpecMoved() {
  local spec_name="$1"

  if [[ $(getChanges | grep -E '^(A|D)' | grep -c "$spec_name") == "2" ]] ; then
    return 0
  fi

  return 1
}

getSpecValue() {
  local spec="$1"
  local macro="$2"

  rpm -q --qf "%{$macro}\n" --specfile "$spec" 2> /dev/null | head -1
}

getNameFromSpec() {
  basename "$1" | sed 's/.spec//'
}

createChangesCache() {
  changes_cache=$(mktemp "/tmp/release-XXXXXXXXX.tmp")
  git diff --name-status master | tr '\t' ' ' | grep -v ' tests/' | grep -Ev '^R100' | grep '\.spec' | sort -k 2 -t ' ' > "$changes_cache"
}

clearChangesCache() {
  rm -f "$changes_cache" 2> /dev/null
}

################################################################################

main "$@"
