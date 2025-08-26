from setuptools import find_packages,setup
from typing import List

# Imports type hints. List[T] is the generic list type (works on older Python versions); 
# Optional[T] means T | None — a value that can be either a T or None. 
# These affect static type checkers (mypy, Pyright) only; Python ignores them at runtime.

HYPEN_E_DOT='-e .' # creating constant to skip reading -e . as a package by mistake
def get_requirements(file_path:str)->List[str]:

# (file_path: str) — the parameter list: file_path is the parameter name.
# : str is a type annotation saying you (the programmer) expect file_path to be a string 
# This is informational for humans and static tools (mypy, linters). Python itself does not enforce it at runtime.
# -> List[str] — the return type annotation:
# It indicates the function is expected to return a List of str values (i.e., ["pkgA==1.2.3", "pkgB"])
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        # while reading line by line in requirements newline character would be added, so we get rid of that
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
name='mlproject',
version='0.0.1',
author='Aishik',
author_email='aishik60@outlook.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')

)