from Cython.Build import cythonize
from setuptools import setup

setup(name="optimised_root", ext_modules=cythonize("root.pyx", annotate=True))
