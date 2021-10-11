from setuptools import setup

setup(
    name='wtf_converter',
    version='1.0.0',
    author="Dezorgon",
    python_requires=">=3.6",
    packages=['parsers.json_parser', 'parsers.toml_parser',
              'parsers.yaml_parser', 'parsers.pickle_parser',
              'serializer_creator']
)