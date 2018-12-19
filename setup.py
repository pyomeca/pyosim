import yaml
from setuptools import setup

import versioneer

with open("environment.yml", 'r') as stream:
    out = yaml.load(stream)
    requirements = out['dependencies'][1:]  # we do not return python

setup(
    name='pyosim',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Pyomeca visualization toolkit",
    author="Romain Martinez",
    author_email='martinez.staps@gmail.com',
    url='https://github.com/pyomeca/pyoviz',
    license='Apache 2.0',
    packages=['pyosim'],
    install_requires=requirements,
    keywords='pyosim',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
