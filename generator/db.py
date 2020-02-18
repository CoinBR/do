import os, inspect

DIRS = {}
DIRS['scripts'] = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DIRS['do'] = os.path.dirname(DIRS['scripts'])
DIRS['project'] = os.path.dirname(DIRS['do'])
DIRS['templates'] = DIRS['scripts'] + '/templates'
DIRS['templates-prefixes'] = DIRS['templates'] + '/prefixes'



# Docker imgs that don't follow a name convention
# that would enable this script to determine 
# the imgs' lang and linux distro
EXTRA_IMGS = {
        # Generic/Hollow image, used when there's not docker-compose file
        # Used when we the project is only a master project
        # that only wants to run its submodules
        'hello-world': {
            'lang': '',
            'distro': 'debian',
            },


        'rabbitmq:3': {
            'lang': '',
            'distro': 'debian'
            },
        }

LANGS = {

        # Used when the image will not execute any custom script in any language
        # Or when its a hollow/parent-only project
        '':  {
            'images': [],
            'extensions': [],
            'test_cmd': '',
            },

        'python': {
            'images': ['python', ],
            'extensions': ['py'],
            'test_cmd': 'pytest',
            },

        'node': {
            'images': ['node', ],
            'extensions': ['js', 'jsx', 'ts'],
            'test_cmd': 'npm test',
            },

        }




DISTROS = {
        'debian': {
            'versions': ['buster', 'stretch', 'jessie', 'wheezy'],
            'cmd': 'bash',
            'pacman': 'apt-get update && apt-get install -y '
            },

        'alpine': {
            'versions': ['alpine'],
            'cmd': 'sh',
            'pacman': 'apk update && apk add --allow-untrusted '
            }
        }

