import os
import setuptools

with open('README.md') as fh:
    long_description = fh.read()

version = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'ahpy', '__version__.py')) as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="ahpy",
    version=version['__version__'],
    author="Philip Griffith",
    author_email="philip.griffith@gmail.com",
    description="A Python implementation of the Analytic Hierarchy Process",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PhilipGriffith/AHPy",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='ahp, mcdm, mcda',
    install_requires=[
        'numpy',
        'scipy'
    ],
    python_requires='>=3.7, <4'
)
