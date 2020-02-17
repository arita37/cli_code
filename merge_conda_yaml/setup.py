import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="merge-conda-yaml",
    version="0.0.6",
    author="Hassan Ahmed",
    author_email="ahmed.hassan.112.ha@gmail.com",
    description="A script to merge multiple anaconda yaml files into one.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blueshack112/merge-conda-yaml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["merge_conda_yaml"],
    entry_points={
        'console_scripts': [
            'merge-conda-yaml=merge_conda_yaml:main',
        ],
    },


)
