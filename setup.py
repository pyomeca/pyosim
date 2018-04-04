from setuptools import setup

requirements = [
    # package requirements go here
]

setup(
    name='pyosim',
    version='0.1.0',
    description="Interface between OpenSim and the Pyomeca library.",
    author="Romain Martinez & Pariterre",
    author_email='martinez.staps@gmail.com',
    url='https://github.com/pyomeca/pyosim',
    packages=['pyosim'],
    install_requires=requirements,
    keywords='pyosim',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
