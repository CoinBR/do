#!/bin/bash
cd "$(dirname "$0")"

if (( $EUID != 0 )); then
  docker-compose run sgl-login-sv sh
  exit
fi
docker-compose run -u 0 sgl-login-sv sh

