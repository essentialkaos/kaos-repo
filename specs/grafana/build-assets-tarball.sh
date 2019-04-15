#!/usr/bin/env bash

################################################################################

APP=$(basename "$0")
VERSION="1.0.0"
DESCR="Tool for building Grafana assets to release tarball"

###############################################################################

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

CL_NORM="\033[${NORM}m"
CL_BOLD="\033[${BOLD}m"
CL_UNLN="\033[${UNLN}m"
CL_RED="\033[${RED}m"
CL_GREEN="\033[${GREEN}m"
CL_BROWN="\033[${BROWN}m"
CL_BLUE="\033[${BLUE}m"
CL_MAG="\033[${MAG}m"
CL_CYAN="\033[${CYAN}m"
CL_GREY="\033[${GREY}m"
CL_BL_RED="\033[${RED};1m"
CL_BL_GREEN="\033[${GREEN};1m"
CL_BL_BROWN="\033[${BROWN};1m"
CL_BL_BLUE="\033[${BLUE};1m"
CL_BL_MAG="\033[${MAG};1m"
CL_BL_CYAN="\033[${CYAN};1m"
CL_BL_GREY="\033[${GREY};1m"
CL_UL_RED="\033[${RED};4m"
CL_UL_GREEN="\033[${GREEN};4m"
CL_UL_BROWN="\033[${BROWN};4m"
CL_UL_BLUE="\033[${BLUE};4m"
CL_UL_MAG="\033[${MAG};4m"
CL_UL_CYAN="\033[${CYAN};4m"
CL_UL_GREY="\033[${GREY};4m"
CL_BG_RED="\033[${RED};7m"
CL_BG_GREEN="\033[${GREEN};7m"
CL_BG_BROWN="\033[${BROWN};7m"
CL_BG_BLUE="\033[${BLUE};7m"
CL_BG_MAG="\033[${MAG};7m"
CL_BG_CYAN="\033[${CYAN};7m"
CL_BG_GREY="\033[${GREY};7m"

################################################################################

# Grafana version
VERSION="$1"

# Path to temporary directory with build data
BUILDROOT=$(mktemp -d /tmp/XXXXXXXX)

# URL to remote repository (HTTP/HTTPS)
REPO_URL="https://github.com/grafana/grafana"

# Path to directory to save release tarball
RELEASE_DIR="$(pwd)/SOURCES"

# Path to release tarball
RELEASE_PATH="${RELEASE_DIR}/grafana-assets-${VERSION}.tar.gz"

################################################################################

export PATH=${BUILDROOT}/node_modules/yarn/bin:${BUILDROOT}/node_modules/grunt/bin:${PATH}

################################################################################
# Print coloured message to terminal
#
# 1: Message (String)
#
# Code: No
# Echo: No
show() {
    if [[ -n "$2" && -z "$no_colors" ]] ; then
        echo -e "\033[${2}m${1}\033[0m"
    else
        echo -e "$1"
    fi
}

# Print error and exit with given message
#
# 1: Message (String)
#
# Code: Yes
# Echo: Yes
printErrorAndExit() {
  show "Error: $1" "$RED"
  exit 1
}

# Show usage message
#
# Code: No
# Echo: Yes
usage() {
  show ""
  show "${CL_BOLD}Usage:${CL_NORM} $APP ${CL_BROWN}version${CL_NORM}"
  show ""
  show "$DESCR"
  show ""
  show "${CL_BOLD}Examples:${CL_NORM}"
  show ""
  show "  $APP 5.4.3"
  show "  $APP 6.0.2"
  show ""
}

# Check if program exists, otherwise exit
#
# *: Command list (Array)
#
# Code: Yes
# Echo: Yes
checkDeps() {
  for p in $@ ; do
    if ! type "$p" >/dev/null ; then
      printErrorAndExit "unable to find program: $p"
      return 1
    fi
  done

  return
}

# Check if parameters are properly specified
#
# Code: Yes
# Echo: Yes
checkArgs() {
  [[ -z "$VERSION" ]] && usage && exit
}

# Clone repository and switch to given tag
#
# 1: Repository URL (String)
# 2: Tag (String)
#
# Code: Yes
# Echo: Yes
cloneRepo() {
  local repo tag

  repo="$1"
  tag="$2"

  git clone --depth=1 -b "$tag" "$repo" "${BUILDROOT}"
}

# Install NodeJS modules using YARN
#
# Code: Yes
# Echo: Yes
installModules() {
  npm --no-color install yarn && \
  yarn --no-color --ignore-engines --pure-lockfile install
}

# Build assets
#
# Code: Yes
# Echo: Yes
buildAssets() {
  grunt --no-color
}

# Create tar.gz archive with prebuilt assets
#
# 1: Path to archive (String)
#
# Code: Yes
# Echo: No
createRelease() {
  local path

  path="$1"

  tar czf "$path" "public/build" "public/views"
}

# Prepare environment for building
#
# Code: Yes
# Echo: No
setup() {
  show "Checking dependencies" "$BOLD"
  checkDeps node npm git

  show "Creating release directory" "$BOLD"
  mkdir -p "${RELEASE_DIR}/"
}

# Finish build process
#
# Code: Yes
# Echo: No
teardown() {
  show "Cleaning up buildroot" $BOLD
  rm -rf "${BUILDROOT}"
}

################################################################################

# Main entrypoint
main() {
  checkArgs

  setup

  cd "${BUILDROOT}" || exit

  show "Fetching source code (v${VERSION})" "$BOLD"
  cloneRepo "${REPO_URL}" "v${VERSION}"

  show "Installing NodeJS modules" "$BOLD"
  installModules

  show "Building assets" "$BOLD"
  buildAssets

  show "Creating release tarball" "$BOLD"
  createRelease "${RELEASE_PATH}"

  cd "${OLDPWD}" || exit

  teardown

  show "Result saved to ${CL_BOLD}${RELEASE_PATH}${CL_NORM}"

  show "Complete" "$GREEN"
}

################################################################################

trap teardown SIGTERM
trap teardown SIGINT

main "$@"

