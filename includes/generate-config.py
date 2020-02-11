import inspect, os
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DO_DIR = os.path.dirname(SCRIPT_DIR)
PROJ_DIR = os.path.dirname(DO_DIR)

# Docker imgs that don't follow a name convention
# that would enable this script to determine 
# the imgs' lang and linux distro
EXTRA_IMGS = {
        'rabbitmq:3': {
            'lang': None,
            'distro': 'debian'
            },
        }

MAP_LANG_IMG = {
        'python': 'python'
        }

MAP_DISTRO_VERSIONS_CMD_PACMAN = {
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
    
    with open(r'{}/Dockerfile'.format(PROJ_DIR)) as f:
        return f.readline()[5:]



def get_cmd_n_pacman(s):
    my_suffix = s.split(':')[1].split('-')[1]
    for distro_name, distro in MAP_DISTRO_VERSIONS_CMD_PACMAN.items():
        distro_keywords = [distro_name] + distro['versions']
        for kw in distro_keywords:
            if kw in my_suffix:
                    return distro['cmd'], distro['pacman']

    raise ValueError("[ERROR] Theres no Docker image with the suffix \"{}\" registered in our dict/JSON/database".format(my_suffix))
 
def get_lang(s):
    my_img_name = s.split(':')[0] 
    for lang in MAP_LANG_IMG.keys():
        for img_name in MAP_LANG_IMG[lang]:
            if img_name in my_img_name:
                return lang

    raise ValueError("[ERROR] Docker image \"{}\" not registered in our dict/JSON/database".format(my_img_name))


def get_all(svc):

    my_img_name = get_docker_img_str(svc)

    def in_extras():
        for img_name in EXTRA_IMGS.keys():
            if img_name in my_img_name:
                lang = EXTRA_IMGS[img_name]['lang']

                distro_name = EXTRA_IMGS[img_name]['distro']
                distro = MAP_DISTRO_VERSIONS_CMD_PACMAN[distro_name]
                cmd, pacman = distro['cmd'], distro['pacman']

                return cmd, pacman, lang
        return False

    if not in_extras():
        cmd, pacman = get_cmd_n_pacman(my_img_name)
        lang = get_lang(my_img_name)
        return cmd, pacman, lang 


def main():
    with open(r'{}/docker-compose.yml'.format(PROJ_DIR)) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        yml = yaml.load(file, Loader=yaml.FullLoader)
        svc_name = next(iter(yml['services']))
        svc = yml['services'][svc_name]
        cmd, pacman, lang = get_all(svc)
        print(get_all(svc))

main()
