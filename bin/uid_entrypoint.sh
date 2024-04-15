#!/bin/sh

#
# OpenShift uses a random UID, which means Python cannot find the user in the /etc/passwd file. This script adds a new
# entry to the /etc/passwd file.
# This script aims to avoid errors like this when the Docker image is deployed to OpenShift:
# getpwuid(): uid not found: 1050370000
#
# WARNING:
# This file must use Unix style line endings (LF), not Windows style line endings (CRLF). Kubernetes will fail to deploy
# if it uses CRLF, stating the reason:
#   starting container process caused: exec: \"uid_entrypoint.sh\": executable file not found in $PATH".
# Adding the following line to .gitattributes forces Git to use UNIX line endings (/n) in shell scripts:
#   *.sh text eol=lf
# shellcheck disable=SC2039
if ! whoami &> /dev/null; then
  if [ -w /etc/passwd ]; then
    echo "${USER_NAME:-default}:x:$(id -u):0:${USER_NAME:-default} user:${HOME}:/sbin/nologin" >> /etc/passwd
  fi
fi

exec "$@"