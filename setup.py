from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

source = [
    "cpptrack/cpptrack.pyx",
    "cpptrack/trackingmodule.cpp",
    "cpptrack/CompressiveTracker.cpp",
    "cpptrack/CompressiveTrackerModule.cpp",
    "cpptrack/BidirectionTrackerModule.cpp",
    "cpptrack/RandomFullTracker.cpp",
]

extensions = Extension(
    "cpptrack",
    sources=source,
    libraries=["opencv_highgui", "opencv_core", "opencv_imgproc"],
    language="c++",
)

setup(
    name = "tracking",
    author = "John Doherty",
    packages = ["tracking", "pytrack"],
    ext_modules = cythonize(extensions),
)
