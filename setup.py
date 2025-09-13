import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="ppfind",
    version="1.0.0",
    author="Disapole",
    author_email="disapolexiao@gmail.com",
    description="A command-line tool to find paper citations, ArXiv links, and GitHub repository links easily.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords=["papers", "citations", "arxiv", "github", "search", "cli","api","academic"],
    url="https://github.com/Disapole-Xiao/ppfind",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ppfind = ppfind.cli:main",
        ],
    },
)