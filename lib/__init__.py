from configparser import ConfigParser, ExtendedInterpolation
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree
from zipfile import ZipFile, ZIP_DEFLATED
import os

def quote_lists(**kwargs):
    for key, value in kwargs.iteritems():
        if ',' in value:
            items = value.split(',')
            kwargs[key] = ','.join(['"{}"'.format(x) for x in items])
    return kwargs

def zip_mod(path, zip_handle):
    for root, dirs, files in os.walk(path):
        print root
        for file in files:
            zip_handle.write(os.path.join(root, file))

def fill_template(env, template, **kwargs):
    return env.get_template(template).render(**kwargs)

def init_conf():
    conf = ConfigParser()
    conf._interpolation = ExtendedInterpolation()
    conf.read('./conf.ini')
    return conf

def initialize(**kwargs):
    conf = init_conf()
    res = conf.get("base_paths", "resources")
    mpt = conf.get("base_paths", "mods")
    mod = '{}/{}'.format(mpt, kwargs['modname'])
    try:
        copytree(res, mod)
    except OSError:
        return False;
    kwargs = quote_lists(**kwargs)
    env = Environment(loader=FileSystemLoader(res), trim_blocks=True)
    for label, path in conf.items("paths"):
        with open('{}/{}'.format(mod, path), 'w+') as new_file:
            new_file.write(fill_template(env, path, **kwargs))
    zip_handle = ZipFile('{}.zip'.format(mod), 'w', ZIP_DEFLATED)
    zip_mod(mod, zip_handle)
    zip_handle.close()
    rmtree(mod)
    return True;
