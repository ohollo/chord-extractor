import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

version = {}
with open("...sample/version.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="chord-extractor",
    version=version,
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
        'librosa', 'vamp'
    ]
)