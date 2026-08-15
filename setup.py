"""Cython build configuration for ZDX PyxelVM."""

from setuptools import setup, find_packages
from Cython.Build import cythonize
from setuptools.extension import Extension
import numpy as np

_COMPILER_DIRECTIVES = {
    "language_level": 3,
    "boundscheck": False,
    "wraparound": False,
}

_NUMPY_INC = [np.get_include()]

extensions = [
    Extension(
        name="zdx_parallel_vm",
        sources=["zdx_parallel_vm.py"],
        include_dirs=_NUMPY_INC,
    ),
    Extension(
        name="zdx_spatial_frame",
        sources=["zdx_spatial_frame.py"],
        include_dirs=_NUMPY_INC,
    ),
    Extension(
        name="zdx_pixel_memory.codec",
        sources=["zdx_pixel_memory/codec.py"],
        include_dirs=_NUMPY_INC,
    ),
    Extension(
        name="zdx_pixel_memory.store",
        sources=["zdx_pixel_memory/store.py"],
    ),
    Extension(
        name="zdx_pixel_memory.spatial_store",
        sources=["zdx_pixel_memory/spatial_store.py"],
    ),
    Extension(
        name="zdx_pixel_memory.agent_memory",
        sources=["zdx_pixel_memory/agent_memory.py"],
    ),
]

setup(
    name="open-pyxel",
    version="1.1.0",
    description="Parallel Pyxel VM with spatial PNG execution and storage",
    packages=find_packages(exclude=["test*"]),
    ext_modules=cythonize(
        extensions,
        compiler_directives=_COMPILER_DIRECTIVES,
        annotate=False,
    ),
    zip_safe=False,
)
