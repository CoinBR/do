try_launch_in_submodules('pull')

run([
    'git pull --recurse-submodules --jobs 4',
    'git submodule update --init --recursive --jobs 4',
    'git add .gitmodules',
    'git add submodules',
    'git commit -m "Updating submodules" && git push origin HEAD',
 ]



