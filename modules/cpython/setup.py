from distutils.core import setup, Extension

setup(name = "tinypy",
      version = "0.8",
      description = "tinypy module for CPython",
      author = "Denis Kasak",
      author_email = "denis.kasak@gmail.com",
      url = "http://www.tinypy.org/",
      ext_modules = [Extension("tinypy", ["cpython.c"], define_macros = [('CPYTHON_MOD', None)])])
