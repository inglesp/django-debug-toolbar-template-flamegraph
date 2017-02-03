from setuptools import find_packages, setup

import os
import re


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, *parts)) as f:
        return f.read()


VERSION = re.search(
    "^__version__ = '(.*)'$",
    read('src', 'template_flamegraph', '__init__.py'),
    re.MULTILINE
).group(1)

if __name__ == '__main__':
    setup(
        name='django-debug-toolbar-template-flamegraph',
        version=VERSION,
        description='Template flamegraphs for Django Debug Toolbar',
        long_description=read('README.md'),
        packages=find_packages(where='src'),
        package_dir={'': 'src'},
        install_requires=['django-debug-toolbar'],
        include_package_data=True,
        zip_safe=False,
        url='http://github.com/inglesp/django-debug-toolbar-template-flamegraph',
        author='Peter Inglesby',
        author_email='peter.inglesby@gmail.com',
        license='License :: OSI Approved :: MIT License',
    )
