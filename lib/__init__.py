from configparser import ConfigParser, ExtendedInterpolation
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree, move
from zipfile import ZipFile, ZIP_DEFLATED
import os

def quote_lists(**kwargs):
    for key, value in kwargs.iteritems():
        if ',' in value:
            items = value.split(',')
            pat = '{0}' if items[0].isdigit() else '"{0}"'
            kwargs[key] = ','.join([pat.format(x.strip()) for x in items])
        if key not in ['modname', 'encountertext']:
            kwargs[key].replace(' ', '\\n')
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
    mod = '{0}/{1}'.format(mpt, kwargs['modname'])
    try:
        copytree(res, mod)
    except OSError:
        return False;
    kwargs = quote_lists(**kwargs)
    env = Environment(loader=FileSystemLoader(res), trim_blocks=True)
    for label, path in conf.items("paths"):
        with open('{0}/{1}'.format(mod, path), 'w+') as new_file:
            new_file.write(fill_template(env, path, **kwargs))
    for i, wave in enumerate(kwargs['possible_attacks'].split(',')):
	move('{0}/Lua/Waves/wave{1}.lua'.format(mod, i+1), '{0}/Lua/Waves/{1}.lua'.format(mod, wave.replace('"', '')))
    zip_handle = ZipFile('{0}.zip'.format(mod), 'w', ZIP_DEFLATED)
    zip_mod(mod, zip_handle)
    zip_handle.close()
    rmtree(mod)
    return True;
