import yaml

from directories import DIRS


DIRS['scripts'], DO_DIR, DIRS['project']

# Docker imgs that don't follow a name convention
# that would enable this script to determine 
# the imgs' lang and linux distro
EXTRA_IMGS = {
        'rabbitmq:3': {
            'lang': None,
            'distro': 'debian'
            },
        }

LANGS = {
        'python': {
            'images': ['python'],
            'test_cmd': ''
            }
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

def get_docker_img_str(svc):
    if ('image' in svc.keys()):
        return svc['image'] 
    
    with open(r'{}/Dockerfile'.format(DIRS['project'])) as f:
        return f.readline()[5:]



def get_distro(s):
    my_suffix = s.split(':')[1].split('-')[1]
    for distro_name, distro in DISTROS.items():
        distro_keywords = [distro_name] + distro['versions']
        for kw in distro_keywords:
            if kw in my_suffix:
                    return distro

    raise ValueError("[ERROR] Theres no Docker image with the suffix \"{}\" registered in our dict/JSON/database".format(my_suffix))
 
def get_lang(s):
    my_img_name = s.split(':')[0] 
    for langname, lang in LANGS.items():
        for img_name in lang['images']:
            if img_name in my_img_name:
                return lang

    raise ValueError("[ERROR] Docker image \"{}\" not registered in our dict/JSON/database".format(my_img_name))


def get_all(svc):

    my_img_name = get_docker_img_str(svc)

    def in_extras():
        for img_name in EXTRA_IMGS.keys():
            if img_name in my_img_name:
                lang_name = EXTRA_IMGS[img_name]['lang']
                lang = LANGS[lang_name]

                distro_name = EXTRA_IMGS[img_name]['distro']
                distro = DISTROS[distro_name]
                
                return distro, lang
        return False

    extra = in_extras()

    if extra:
        distro, lang = extra
    else:
        distro, lang = get_distro(my_img_name), get_lang(my_img_name)

    return {'distro': distro,
            'lang': lang,
            'service': svc
            }



def get_cfg():
    with open(r'{}/docker-compose.yml'.format(DIRS['project'])) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        yml = yaml.load(file, Loader=yaml.FullLoader)
        svc_name = next(iter(yml['services']))
        svc = yml['services'][svc_name]
        return get_all(svc)

