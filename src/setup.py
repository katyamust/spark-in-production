
from setuptools import setup, find_packages

__version__ = ""
with open('VERSION') as version_file:
    __version__ = version_file.read().strip()

setup(name='spark_utils',
      version=__version__,
      description='Streaming and aggregation of sample meter data',
      long_description="",
      long_description_content_type='text/markdown',
      license='MIT',
      packages=find_packages()
      )
