PULLCMD = 'git pull --recurse-submodules --jobs 4'

run(PULLCMD)
run('git submodule update --init --recursive --jobs 4')
run(PULLCMD, cd=dirs['do'])

try_launch_in_submodules('pull')

run([
    'git add .gitmodules',
    'git add submodules',
    'git add do'
    'git commit -m "Update submodules" && git push origin HEAD',
 ])
