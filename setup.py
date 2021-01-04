# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Dana Lehman
# Copyright (c) 2020, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


import sys
if sys.version_info < (3, 6):
    sys.exit('text2cc requires Python 3.6+')
import pathlib
from setuptools import setup, find_packages




# Extract the version from version.py, using functions in fmtversion.py
fmtversion_path = pathlib.Path(__file__).parent / 'text2cc' / 'fmtversion.py'
exec(compile(fmtversion_path.read_text(encoding='utf8'), 'text2cc/fmtversion.py', 'exec'))
version_path = pathlib.Path(__file__).parent / 'text2cc' / 'version.py'
version = get_version_from_version_py_str(version_path.read_text(encoding='utf8'))

readme_path = pathlib.Path(__file__).parent / 'README.md'
long_description = readme_path.read_text(encoding='utf8')


setup(name='text2cc',
      version=version,
      py_modules=[],
      packages=find_packages(),
      package_data = {},
      description='Create quizzes in Common Cartridge   format from Markdown-based plain text',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Dana Lehman',
      author_email='',
      url='http://github.com/dlehman83/text2cc',
      license='BSD',
      keywords=['QTI', 'IMS Question & Test Interoperability', 'quiz', 'test',
          'exam', 'assessment', 'markdown', 'LaTeX', 'plain text','Common Cartridge'],
      python_requires='>=3.6',
      install_requires=[
          'bespon>=0.4',
          'markdown>=3.2',
      ],
      # https://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Education',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Education :: Testing',
      ],
      entry_points = {
          'console_scripts': ['text2cc = text2cc.cmdline:main'],
          'gui_scripts': ['text2cc_tk = text2cc.gui.tk:main'],
      },
)
