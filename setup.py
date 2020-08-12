from setuptools import setup
from pathlib import Path

README_path = Path.cwd() / 'README.md'
with open(README_path, 'r') as README_f:
    README = README_f.read()

setup(
    name='confIDent Data imports',
    version='0.1.0',
    packages=['dataimports', 'dataimports/wikidata'],
    url='',
    license='MIT License',
    author='Andre Castro',
    author_email='andre.castro@tib.eu',
    description='Application imports external sources of Scientific Events '
                'and Scientific Events Series on to confIDdent',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 3.7'],
    keywords='spaql wikidata semantic',
    install_requires=['SPARQLWrapper', 'pyyaml', 'Jinja2', 'mediawikitools'],
    test_require=['pytest']
)
