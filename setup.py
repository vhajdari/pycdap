from setuptools import setup, find_packages

setup(
    name='pycdap',
    version='0.1',
    # packages=[''],
    # py_modules=['Pipeline'],
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='Apache 2.0',
    author='Tony Hajdari',
    author_email='tony@cask.co',
    description='CDAP python library for exporting pipelines',
    install_requires=[
        'Click',
        'requests'
     ],
    entry_points='''
         [console_scripts]
         piper=cli.pipeline_cli:piper
     '''
)
