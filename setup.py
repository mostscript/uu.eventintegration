from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='uu.eventintegration',
      version=version,
      description="UPIQ.org integration of plone.app.event into Plone 4.2.",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone event',
      author='Plone Foundation',
      maintainer_email='sean.upton@hsc.utah.edu',
      url='https://github.com/seanupton/uu.eventintegration',
      license='GPL',
      packages=find_packages(),
      namespace_packages=['uu'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.dexterity',
          'plone.directives.form',
          'plone.app.event[dexterity]',
          'Solgema.fullcalendar',
          'z3c.unconfigure',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """)
