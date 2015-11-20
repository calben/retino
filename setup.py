from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='retino',
      version='0.0.1',
      description=u"Model of Retinal Activity and Axonal Growth",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Calem Bendell",
      author_email='calem.j.bendell@gmail.com',
      url='https://github.com/calben/retino',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      extras_require={
          'test': ['pytest'],
      },
      # entry_points="""
      # [console_scripts]
      # pyskel=pyskel.scripts.cli:cli
      # """
      )
