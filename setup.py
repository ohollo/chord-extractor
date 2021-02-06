import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = {}
with open('chord_extractor/version.py') as fp:
    exec(fp.read(), version)

try:
    import numpy
except ModuleNotFoundError:
    raise ModuleNotFoundError('Please install numpy prior to installing this package, so that setup.py of vamp '
                              'package can run. See README for details')

setuptools.setup(
    name="chord-extractor",
    version=version['__version__'],
    author="Oliver Holloway",
    author_email="author@example.com",
    description="A small example package",
    long_description="A long description",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
    ],
    package_data={'chord_extractor': ['_lib/nnls-chroma.so']}
)