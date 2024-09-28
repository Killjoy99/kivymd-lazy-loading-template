from Cython.Build import cythonize
from setuptools import Extension, setup

ext_modules = Extension(
    "src.to_optimise_module",
    ["src/module/to/optimise"],
    define_macros=[("CYTHON_LIMITED_API", "1")],
    py_limited_api=True,
)

setup(ext_modules=cythonize(ext_modules))
