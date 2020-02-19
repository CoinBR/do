PULL = 'git pull --recurse-submodules --jobs 4'
CHECKOUT = 'git checkout HEAD || git checkout master'

run(CHECKOUT)
run('git submodule update --init --recursive --jobs 4')
run([CHECKOUT, PULL, 'generator/generate.py'], cd=dirs['do'])


try_launch_in_submodules('pull')

run([
    'git add .gitmodules',
    'git add submodules',
    'git add do'
    'git commit -m "Update submodules" && git push origin HEAD',
 ])
