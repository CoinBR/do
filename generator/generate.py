#!/usr/bin/env python3

import os
import re
from os.path import isfile, join
from collections import deque as dq
from functools import reduce


from db import DIRS, DISTROS, LANGS
from get_cfg import get_cfg

CFG = get_cfg()


def make_path(directory, filename, change_extension_to=False):
    # scripts in "DO" directory should not have an extension
    if directory == DIRS['do'] and change_extension_to == False:
        return make_path(directory, filename, '')
 
    fnx = try_split_filename_extension(filename) 
    ext = change_extension_to if change_extension_to != False else fnx[1]
    myfnx = join_filename_extension([fnx[0], ext]) if ext != '' else fnx[0]
    return directory + '/' + myfnx
    

def make_paths(directory, filenames, change_extension_to=False):
    return dq(map(lambda f: make_path(directory, f, change_extension_to), filenames))

def try_delete_file(path: str):
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


def list_files(directory):
    return [f for f in os.listdir(directory) if isfile(join(directory, f))]

def try_split_filename_extension(s):
    if isinstance(s, str):
        if '.' in s:
            return s.split('.') 
        else:
            return [s, '']
    return s # already split

def join_filename_extension(lst):
    return '{}.{}'.format(lst[0], lst[1]) 

def is_valid_fn(filename):
    return not (len(try_split_filename_extension(filename)) != 2 
                or filename[0] == '.'
                or filename[-4:] == '.swp')

def apply_syntax(s):


    def get_replace_value(match): 
        dict_path = [CFG] + match.split('.')
        return reduce(lambda k, v: k[v.lower()], dict_path)

    matches = re.findall(re.compile(r'{{{(.*?)}}}'), s)
    for match in matches:
        curly = '{{{' + match + '}}}'
        s = s.replace(curly, get_replace_value(match))
    return s 


def gen_file(sourcefilename):
    filename, ext = try_split_filename_extension(sourcefilename)
    
    with open(make_path(DIRS['templates'], sourcefilename), 'r') as f_template:
        with open(make_path(DIRS['templates-prefixes'], ext), 'r') as f_prefix:
            with open(make_path(DIRS['do'], filename), 'w+') as f_generated:
                contents = map(apply_syntax, [f_prefix.read(), f_template.read()] )
                dq(map(f_generated.write, contents ))


def gen_all():

    sourcefilenames = list(filter(is_valid_fn, list_files(DIRS['templates'])))
    dq(map(try_delete_file, make_paths(DIRS['do'], sourcefilenames, change_extension_to='')))
    dq(map(gen_file, sourcefilenames))
    os.system('chmod +x {}/*'.format(DIRS['do'])) # make scripts executable


def main():
    gen_all()

main()
