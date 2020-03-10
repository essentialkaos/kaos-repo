#!/bin/bash

DL_BASE="https://download.maxmind.com/app/geoip_download?suffix=zip&license_key=$MM_LICENSE_KEY"

main() {
  if [[ -z "$MM_LICENSE_KEY" ]] ; then
    echo "Usage: MM_LICENSE_KEY=YOUR_LICENSE_KEY ./getfiles.sh"
    exit 1
  fi

  curl -# -o SOURCES/GeoLite2-City-CSV.zip    "${DL_BASE}&edition_id=GeoLite2-City-CSV"
  curl -# -o SOURCES/GeoLite2-Country-CSV.zip "${DL_BASE}&edition_id=GeoLite2-Country-CSV"
  curl -# -o SOURCES/GeoLite2-ASN-CSV.zip     "${DL_BASE}&edition_id=GeoLite2-ASN-CSV"
}

main "$@"
