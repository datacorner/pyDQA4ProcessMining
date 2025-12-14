#!/usr/bin/env python3
"""
Setup script for pyDQA4ProcessMining.

This allows installation via pip:
    pip install .
    pip install -e .  # Development mode
"""

from setuptools import setup, find_packages
import os

# Read version from package
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'pydqa4pm', '__init__.py')
    with open(version_file, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')
    return '1.0.0'

# Read README for long description
def get_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='pydqa4pm',
    version=get_version(),
    author='Benoit CAYLA',
    author_email='benoit@datacorner.fr',
    description='Data Quality Assessment Tool for Process Mining',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/datacorner/pyDQA4ProcessMining',
    license='GPL',
    
    packages=find_packages(exclude=['tests', 'samples', 'docs']),
    include_package_data=True,
    
    python_requires='>=3.10',
    
    install_requires=[
        'pandas>=1.5.0',
        'numpy>=1.23.0',
        'matplotlib>=3.6.0',
        'seaborn>=0.12.0',
        'fpdf>=1.7.2',
    ],
    
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'flake8>=6.0.0',
            'black>=23.0.0',
            'mypy>=1.0.0',
        ],
    },
    
    entry_points={
        'console_scripts': [
            'pmdqa=pmdqa:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Quality Assurance',
    ],
    
    keywords=[
        'process-mining',
        'data-quality',
        'dqa',
        'csv-validation',
        'data-profiling',
        'pdf-report',
    ],
    
    project_urls={
        'Bug Reports': 'https://github.com/datacorner/pyDQA4ProcessMining/issues',
        'Source': 'https://github.com/datacorner/pyDQA4ProcessMining',
        'Documentation': 'https://github.com/datacorner/pyDQA4ProcessMining/tree/main/docs',
    },
)

