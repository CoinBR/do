if (( $EUID != 0 )); then
  docker-compose run sgl-login-sv {{{lang.test_cmd}}}
  exit
fi
docker-compose run -u 0 sgl-login-sv {{{lang.test_cmd}}}
