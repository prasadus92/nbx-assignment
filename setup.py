import os
import re

from setuptools import setup


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


install_requires = ['aiohttp==3.5.4',
                    'sqlalchemy==1.3.9',
                    'aiohttp_validate==1.1.0',
                    'ujson==1.35',
                    'trafaret==1.2.0',
                    'aiopg==1.0.0',
                    'trafaret-config==2.0.2',
                    'aiohttp_swagger==1.0.9',
                    'formencode==1.3.1'
                    ]

setup(name='userservice',
      version=read_version(),
      description='NBX User Service',
      platforms=['POSIX'],
      author='NBX',
      author_email='developer@nbx.com',
      packages=['userservice', ],
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False,
      )
