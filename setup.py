import versioneer
from setuptools import setup

setup(
    name="dominos",
    author="sralloza",
    license="mit",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
