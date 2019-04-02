import setuptools

with open("readme.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storystructure",
    version="1.0.2",
    author="Diamantis Sellis",
    author_email="sellisd@gmail.com",
    description="Tools for analysing the structure of branching stories",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/sellisd/storystructure",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
    ],
)
