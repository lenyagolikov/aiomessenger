import os
from importlib.machinery import SourceFileLoader

from setuptools import setup, find_packages
from pkg_resources import parse_requirements

module_name = 'messenger'

module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()


def load_requirements(filename):
    """Возвращает список зависимостей из файла"""
    requirements = []
    with open(filename, 'r') as file:
        for req in parse_requirements(file.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    platforms="all",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Operating System :: Linux',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    python_requires='>=3.9',
    packages=find_packages(exclude=["tests"]),
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements.dev.txt')},
    entry_points={
        'console_scripts': [
            f'{module_name}-api = {module_name}.api.__main__:main',
            f'{module_name}-db = {module_name}.db.__main__:main'
        ]
    },
    include_package_data=True
)
