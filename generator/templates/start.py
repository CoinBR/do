BASE_CMD = 'docker-compose down && docker-compose up'

if CFG['service'] != '':
    run(BASE_CMD, argv)

try_launch_in_submodules('start')
