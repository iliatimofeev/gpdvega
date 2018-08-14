# flake8: noqa

import io
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

LONG_DESCRIPTION = """
``gpdvega`` is a bridge between GeoPandas_ a geospatial extension of Pandas_ 
and the declarative statistical visualization library Altair_, 
which allows to seamlessly chart geospatial data.
The source is available on `GitHub <https://github.com/iliatimofeev/gpdvega>`_. 
.. _Pandas: http://pandas.pydata.org/
.. _GeoPandas: http://geopandas.org/
.. _Altair: http://altair-viz.github.io/
"""


# ==============================================================================
# Utilities
# ==============================================================================

def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def get_install_requirements(path):
    content = read(path)
    return [
        req
        for req in content.split("\n")
        if req != '' and not req.startswith('#')
    ]


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py

    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


HERE = os.path.abspath(os.path.dirname(__file__))


# From https://github.com/jupyterlab/jupyterlab/blob/master/setupbase.py,
#  BSD licensed
def find_packages(top=HERE):
    """
    Find all of the packages.
    """
    packages = []
    for d, dirs, _ in os.walk(top, followlinks=True):
        if os.path.exists(os.path.join(d, '__init__.py')):
            packages.append(os.path.relpath(d, top).replace(os.path.sep, '.'))
        elif d != top:
            # Do not look for packages in subfolders if current is not a package
            dirs[:] = []
    return packages

# ==============================================================================
# Variables
# ==============================================================================


DESCRIPTION         = "GpdVega GeoPandas and Altair intergation"
NAME                = "gpdvega"
PACKAGES            = find_packages()
AUTHOR              = "Ilia Timofeev"
AUTHOR_EMAIL        = "ilia.timofeev@gmail.com"
URL                 = 'https://iliatimofeev.github.io/gpdvega/'
DOWNLOAD_URL        = 'https://github.com/iliatimofeev/gpdvega'
LICENSE             = 'BSD 3-clause'
INSTALL_REQUIRES    = get_install_requirements("requirements.txt")
DEV_REQUIRES        = get_install_requirements("requirements_dev.txt")
VERSION             = version(os.path.join(NAME, '__init__.py'))


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=PACKAGES,
      install_requires=INSTALL_REQUIRES,
      extras_require={
        'dev': DEV_REQUIRES
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'],
)
