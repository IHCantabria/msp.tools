from setuptools import setup, find_namespace_packages
from msptools.config import CONFIG


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="msptools",
    version=CONFIG["version"],
    description="Marine Spatial Planning: Aquaculture",
    url="https://github.com/ihcantabria/msptools",
    author="Felipe Maza",
    author_email="felipe.maza@ihcantabria.com",
    license="GPLv3",
    packages=find_namespace_packages(exclude=["contrib", "docs", "tests"]),
    scripts=["msptools/aquaculture.py"],
    install_requires=["siphon==0.8.0"],
    zip_safe=False,
)
