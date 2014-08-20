import glob
import os
import sys
import types
from pathlib import Path


PROJECT_PATH = Path()


def rel(*x):
    return str(PROJECT_PATH.joinpath(*x).absolute())

sys.path.insert(1, str(rel('apps')))


class optional(str):
    pass


def include(*args, **kwargs):
    scope = kwargs.pop("scope")
    including_file = scope.get('__included_file__', scope['__file__'].rstrip('c'))
    confpath = os.path.dirname(including_file)
    for conffile in args:
        saved_included_file = scope.get('__included_file__')
        pattern = os.path.join(confpath, conffile)

        files_to_include = glob.glob(pattern)
        if not files_to_include and not isinstance(conffile, optional):
            raise IOError('No such file: %s' % pattern)

        for included_file in files_to_include:
            scope['__included_file__'] = included_file
            exec(open(included_file).read(), {}, scope)

            modulename = ('_split_settings.%s'
                          % conffile[:conffile.rfind('.')].replace('/', '.'))
            module = types.ModuleType(modulename)
            module.__file__ = included_file
            sys.modules[modulename] = module
        if saved_included_file:
            scope['__included_file__'] = saved_included_file
        elif '__included_file__' in scope:
            del scope['__included_file__']


include(
    'components/base.py',
    'components/auth.py',
    'components/locale.py',
    'components/static.py',
    'components/templates.py',
    'components/db_and_cache.py',
    'components/middleware.py',
    'components/apps.py',
    'components/logging.py',
    'components/libs.py',
    optional('local.py'),
    scope=locals()
)
