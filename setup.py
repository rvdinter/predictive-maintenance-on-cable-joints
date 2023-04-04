from setuptools import setup

setup(
    name="alliander_predictive_maintenance",
    author="Raymon van Dinter",
    author_email="raymon.van.dinter@sioux.eu",
    version="0.0.1",
    install_requires=["matplotlib~=3.6",
                      "pytest~=7.1",
                      "pandas~=1.5",
                      "scikit-learn~=1.1",
                      "jupyter",
                      "seaborn~=0.12",
                      "numpy~=1.24",
                      "requests~=2.28",
                      "openpyxl~=3.1"
                      ],
    packages=["alliander_predictive_maintenance"]
)
