if (( $EUID != 0 )); then
  docker-compose run {{{SERVICE}}} {{{DISTRO.CMD}}}
  exit
fi
docker-compose run -u 0 {{{SERVICE}}} {{{DISTRO.CMD}}}
