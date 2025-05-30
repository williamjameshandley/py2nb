#!/usr/bin/env python3

from setuptools import setup, Command, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


def get_version(short=False):
    with open('README.rst') as f:
        for line in f:
            if ':Version:' in line:
                ver = line.split(':')[2].strip()
                if short:
                    subver = ver.split('.')
                    return '%s.%s' % tuple(subver[:2])
                else:
                    return ver


setup(name='py2nb',
      version=get_version(),
      description='py2nb: convert python scripts to jupyter notebooks',
      long_description=readme(),
      long_description_content_type='text/x-rst',
      author='Will Handley',
      author_email='wh260@cam.ac.uk',
      url='https://github.com/williamjameshandley/py2nb',
      scripts=['py2nb', 'nb2py'],
      py_modules=['py2nb', 'nb2py'],
      install_requires=['nbformat'],
      include_package_data=True,
      license='GPL',
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Natural Language :: English',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   'Programming Language :: Python :: 3.11',
                   'Programming Language :: Python :: 3.12',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Text Processing :: Markup',
                   'Topic :: Scientific/Engineering',
      ],
      python_requires='>=3.7',
      )
