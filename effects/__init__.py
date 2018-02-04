from glob import glob
from os.path import dirname, basename, isfile, join
from importlib import import_module
from collections import namedtuple

__all__ = ['effects']
effects_dict = {basename(path)[0:-3]:import_module('.' + basename(path[0:-3]), __package__)
                for path in glob(join(dirname(__file__), '*.py'))
                if (isfile(path) and not basename(path).startswith("_"))}
effects = namedtuple('effects', effects_dict.keys())(**effects_dict)
