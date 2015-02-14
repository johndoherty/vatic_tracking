from distutils.core import setup 
from distutils.core import Extension

module1 = Extension('tracking',
        sources = ['demo.c'])

setup (name = 'PackageName',
        version = '1.0',
        description = 'This is a demo package',
        ext_modules = [module1])
