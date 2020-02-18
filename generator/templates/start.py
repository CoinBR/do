import os
import sys
from collections import deque as dq


BASE_CMD = 'docker-compose down && docker-compose up'
FLAGS = ' ' + ' '.join(sys.argv) if len(sys.argv) else False

def start(path: str=DIRS['project'], serve: bool=False):
    cmd = BASE_CMD + FLAGS 
    os.system('cd {} && {}'.format(path, cmd))
    try_start_submodules(path)

def try_start_submodules(path: str):
    subroot = path + '/submodules'
    if not (os.path.exists(subroot) and os.path.isdir(subroot)):
        return

    projs = [d for d in os.listdir(subroot) 
            if os.path.isdir(os.path.join(subroot, d))]
    dq(os.system(os.path.join(subroot, proj, 'do')) for proj in projs)
    
if CFG['service'] == '':
    print()
    exit()
