from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize("optimised_root.pyx", language_level="3"),
)
