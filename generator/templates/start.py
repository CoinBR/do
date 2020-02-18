import os
import sys
from collections import deque as dq


BASE_CMD = 'docker-compose down && docker-compose up'
FLAGS = ' ' + ' '.join(sys.argv) if len(sys.argv) else False


def start():
    cmd = BASE_CMD + FLAGS 
    os.system('cd {} && {}'.format(DIRS['project'], cmd))

def try_start_submodules():
    subroot = os.path.join(DIRS['project'], 'submodules')
    if not (os.path.exists(subroot) and os.path.isdir(subroot)):
        return

    projs = [d for d in os.listdir(subroot) 
            if os.path.isdir(os.path.join(subroot, d))]

    dq(os.system(os.path.join(subroot, proj, 'do', 'start') + FLAGS) for proj in projs)
    
if CFG['service'] != '':
    start()

try_start_submodules()