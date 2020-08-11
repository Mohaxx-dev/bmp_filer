import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bmpFiler-jaek", #
    version="0.0.1",#
    author="Bouderbala Mohammed Amine",
    author_email="bouderbalaamine2000@gmail.com",
    description="",#
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="github",#
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)