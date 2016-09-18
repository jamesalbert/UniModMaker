"""
UniModMaker provides an easy way to create mods for Unitale

try it at http://jimmyjam5000.com
"""

from configparser import ConfigParser, ExtendedInterpolation
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree, move
from zipfile import ZipFile, ZIP_DEFLATED
import os


class UniModHelper(object):
    """provides methods to create a unitale mod"""
    def __init__(self, **kwargs):
        self.init_conf()
        self.get_paths(kwargs['modname'])
        copytree(self.resources_path, self.new_mod_path)
        kwargs = self.validate(**kwargs)
        self.fill_templates(**kwargs)
        self.rename_waves(kwargs['possible_attacks'])
        self.zip_mod(self.new_mod_path)
        rmtree(self.new_mod_path)

    def get_paths(self, modname):
        """
        get paths to resources and the mod to be created

        :param modname: the name of the mod
        """
        mods_path = self.conf.get("base_paths", "mods")
        self.resources_path = self.conf.get("base_paths", "resources")
        self.new_mod_path = '{0}/{1}'.format(mods_path, modname)

    def rename_waves(self, possible_attacks):
        """
        rename wave filenames

        :param possible_attacks: the possible attacks (waves)
        """
        for i, wave in enumerate(possible_attacks.split(',')):
            old = '{0}/Lua/Waves/wave{1}.lua'.format(self.new_mod_path, i+1)
            new = '{0}/Lua/Waves/{1}.lua'.format(self.new_mod_path, wave.replace('"', ''))
            move(old, new)

    def validate(self, **kwargs):
        """
        validate breaks up form fields to their respective data structures

        :param kwargs: dictionary of form items
        """
        for key, value in kwargs.items():
            if key in dict(self.conf.items('separable')):
                items = value.split(',')
                pat = '{0}' if items[0].isdigit() else '"{0}"'
                kwargs[key] = ','.join([pat.format(x.strip()) for x in items])
            if key not in dict(self.conf.items('not spaceable')):
                kwargs[key] = kwargs[key].replace(' ', '\\n')
            if key in dict(self.conf.items('radio')):
                kwargs[key] = 'true' if value == 'on' else 'false'
        return kwargs

    def zip_mod(self, path):
        """
        archive the created mod folder

        :param path: path to mod folder
        :param zip_handle: file handle of zip archive
        """
        zip_handle = ZipFile('{0}.zip'.format(self.new_mod_path), 'w', ZIP_DEFLATED)
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_handle.write(os.path.join(root, file))
        zip_handle.close()

    def fill_templates(self, **kwargs):
        """
        fill templates (encounter.lua, etc) with specified values

        :param kwargs: dictionary of form fields
        """
        resfs = FileSystemLoader(self.resources_path)
        env = Environment(loader=resfs, trim_blocks=True)
        for label, path in self.conf.items("paths"):
            with open('{0}/{1}'.format(self.new_mod_path, path), 'w+') as new_file:
                new_file.write(
                    env.get_template(path).render(**kwargs)
                )

    def init_conf(self):
        """
        get a dictionary representing conf.ini
        """
        self.conf = ConfigParser()
        self.conf._interpolation = ExtendedInterpolation()
        self.conf.read('./conf.ini')
