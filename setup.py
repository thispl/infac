from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in infac/__init__.py
from infac import __version__ as version

setup(
	name="infac",
	version=version,
	description="Custom APP for Infac",
	author="teampro",
	author_email="jagadeesan.a@groupteampro.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
