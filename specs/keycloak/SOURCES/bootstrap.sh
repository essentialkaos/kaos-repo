#!/bin/bash

CONFIG="/etc/keycloak/keycloak.conf"

if [[ -f "/etc/sysconfig/keycloak" ]] ; then
  source /etc/sysconfig/keycloak
fi

if ! /var/lib/keycloak/bin/kc.sh --config-file="$CONFIG" bootstrap-admin user ; then
  exit 1
fi

if ! /var/lib/keycloak/bin/kc.sh --config-file="$CONFIG" start-dev ; then
  exit 1
fi

exit 0
