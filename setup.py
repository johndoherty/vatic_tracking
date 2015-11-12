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
    # TLD
    "cpptrack/TldTrackerModule.cpp",
    "cpptrack/TldTracker.cpp",
    "cpptrack/TLD.cpp",
    "cpptrack/tld_utils.cpp",
    "cpptrack/LKTracker.cpp",
    "cpptrack/FerNNClassifier.cpp",
    # BiTLD
    "cpptrack/BiTldTrackerModule.cpp",
]

extensions = Extension(
    "cpptrack",
    sources=source,
    libraries=["opencv_highgui", "opencv_core", "opencv_imgproc", "opencv_legacy"],
    language="c++",
)

setup(
    name = "tracking",
    author = "John Doherty, Charlie Ma",
    packages = ["tracking", "pytrack"],
    ext_modules = cythonize(extensions),
    data_files=[('config', ['./cpptrack/TLDparameters.yml'])]
)
