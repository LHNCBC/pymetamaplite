# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='pymetamaplite',
      version='0.3',
      description='MetaMapLite Entity Recognizer implementation',
      author='Willie Rogers',
      author_email='wjrogers@mail.nih.gov',
      url="https://metamap.nlm.nih.gov/",
      license="Public Domain",
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6')
