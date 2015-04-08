from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
            "tracking",
            sources=["tracking.pyx", "trackingmodule.cpp", "CompressiveTracker.cpp", "CompressiveTrackerModule.cpp", "BidirectionTrackerModule.cpp"],
            libraries=["opencv_highgui", "opencv_core", "opencv_imgproc"],
            language="c++",
        )))
