if (( $EUID != 0 )); then
  docker-compose run {{{service}}} {{{lang.test_cmd}}}
  exit
fi
docker-compose run -u 0 {{{service}}} {{{lang.test_cmd}}}
