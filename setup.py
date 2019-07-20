"""TODO"""
import os

from setuptools import setup, find_packages

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR_PATH, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

name = 'koles'

setup(
    name=name,
    packages=find_packages('src'),
    package_dir={'koles': 'src/koles'},
    package_data={'koles': ['data/swear_list/*.dat']},
    author='myslak71',
    author_email=' ',
    description='Bad language linter',
    long_description=long_description,
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'koles = koles.cli:main',
        ],
    },
)
