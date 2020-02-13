import os, inspect

DIRS = {}
DIRS['scripts'] = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DIRS['do'] = os.path.dirname(DIRS['scripts'])
DIRS['project'] = os.path.dirname(DIRS['do'])

