from setuptools import setup, find_packages

setup(
    name="fridapatcher",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "fridapatcher=fridapatcher.cli:main",
        ],
    },
)