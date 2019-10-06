import os
import re

from setuptools import find_packages, setup


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'userservice', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in userservice/__init__.py'
            raise RuntimeError(msg)


install_requires = ['aiohttp',
                    'aiopg[sa]',
                    'aiohttp_swagger',
                    'trafaret-config']

setup(name='user-service',
      version=read_version(),
      description='NBX User Service',
      platforms=['POSIX'],
      packages=find_packages(),
      install_requires=install_requires,
      zip_safe=False)
