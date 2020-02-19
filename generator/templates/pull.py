run('git pull --recurse-submodules --jobs 4 && git submodule update --init --recursive --jobs 4')
try_launch_in_submodules('pull')
