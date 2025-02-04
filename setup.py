#! /usr/bin/env python

import sys
import os
import io
import shutil
from numpy.distutils.core import setup

descr = """Intra-subject preprocessing of MRI data in pure Python!"""
DISTNAME = 'pyaffineprep'
DESCRIPTION = 'Statistical learning for neuroimaging in Python'
LONG_DESCRIPTION = io.open('README.rst', encoding="utf8").read()
MAINTAINER = 'Elvis Dohmatob'
MAINTAINER_EMAIL = 'gmdopp@gmail.com'
URL = 'http://pyaffineprep.github.com'
LICENSE = 'new BSD'
DOWNLOAD_URL = 'http://pyaffineprep.github.com'
VERSION = '0.1-git'


# For some commands, use setuptools
if len(set(('develop', 'sdist', 'release', 'bdist_egg', 'bdist_rpm',
            'bdist', 'bdist_dumb', 'bdist_wininst', 'install_egg_info',
            'build_sphinx', 'egg_info', 'easy_install', 'upload',
            )).intersection(sys.argv)) > 0:
    from setuptools import setup  # noqa


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    # main modules
    config.add_subpackage('pyaffineprep')

    # extrenal dependecies
    config.add_subpackage('pyaffineprep/externals')
    config.add_subpackage('pyaffineprep/externals/tempita')

    # plugin for generating reports
    config.add_subpackage('pyaffineprep/reporting')
    config.add_data_dir("pyaffineprep/reporting/template_reports")
    config.add_data_dir("pyaffineprep/reporting/css")
    config.add_data_dir("pyaffineprep/reporting/js")
    config.add_data_dir("pyaffineprep/reporting/icons")
    config.add_data_dir("pyaffineprep/reporting/images")

    return config


if __name__ == "__main__":

    old_path = os.getcwd()
    local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    # python 3 compatibility stuff.
    # Simplified version of scipy strategy: copy files into
    # build/py3k, and patch them using lib2to3.
    if sys.version_info[0] == 3:
        try:
            import lib2to3cache  # noqa
        except ImportError:
            pass
        local_path = os.path.join(local_path, 'build', 'py3k')
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        print("Copying source tree into build/py3k for 2to3 transformation"
              "...")
        shutil.copytree(os.path.join(old_path, 'pyaffineprep'),
                        os.path.join(local_path, 'pyaffineprep'))
        import lib2to3.main
        from io import StringIO
        print("Converting to Python3 via 2to3...")
        _old_stdout = sys.stdout
        try:
            sys.stdout = StringIO()  # supress noisy output
            res = lib2to3.main.main("lib2to3.fixes",
                                    ['-x', 'import', '-w', local_path])
        finally:
            sys.stdout = _old_stdout

        if res != 0:
            raise Exception('2to3 failed, exiting ...')

    os.chdir(local_path)
    sys.path.insert(0, local_path)

    setup(configuration=configuration,
          name=DISTNAME,
          maintainer=MAINTAINER,
          include_package_data=True,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          long_description=LONG_DESCRIPTION,
          zip_safe=False,  # the package can run out of an .egg file
          classifiers=[
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'License :: OSI Approved',
              'Programming Language :: C',
              'Programming Language :: Python',
              'Topic :: Software Development',
              'Topic :: Scientific/Engineering',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Operating System :: Unix'
              ]
          )
