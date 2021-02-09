import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = {}
with open('chord_extractor/version.py') as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="chord-extractor",
    version=version['__version__'],
    author="Oliver Holloway",
    author_email="oholloway.consulting@gmail.com",
    description="Python library for extracting chords from multiple sound file formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ohollo/chord-extractor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6,<3.9',
    install_requires=[
        'librosa', 'vamp'
    ],
    package_data={'chord_extractor': ['_lib/nnls-chroma.so']}
)