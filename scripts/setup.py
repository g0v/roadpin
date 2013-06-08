import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, '00README.md')) as f:
    README = f.read()
with open(os.path.join(here, '01CHANGELOG.md')) as f:
    CHANGES = f.read()

requires = [
    ]

setup(name='app',
      version='0.0',
      description='app',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="tests",
      entry_points="""\
      [pyramid.scaffold]
      simple = scripts.templates:SimpleProjectTemplate
      simple_module = scripts.templates:SimpleModuleProjectTemplate
      web = scripts.templates:WebProjectTemplate
      pkg = scripts.templates:PkgProjectTemplate
      """,
      )
