from setuptools import find_packages, setup
from pathlib import Path
from typing import List


def get_requirements(file_path: Path) -> List[str]:
    """
    function that return list of all required packages in the repository

    :param file_path: path to requirements.txt file (filename if file is located in project root)
    :return: List of names of packages to install
    """

    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if '-e .' in requirements:
            requirements.remove('-e .')

    return requirements


setup(
    name='mlengine',
    version='0.0.1',
    author='badutka',
    author_email='toobad3119@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(Path('requirements.txt'))
)
