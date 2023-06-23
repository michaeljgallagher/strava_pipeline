from setuptools import find_packages, setup

setup(
    name="strava_pipeline",
    version="0.1",
    author="Michael Gallagher",
    author_email="mjgall@pm.me",
    maintainer="Michael Gallagher",
    maintainer_email="mjgall@pm.me",
    license="MIT",
    url="https://github.com/michaeljgallagher/strava_pipeline",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    package_data={
        "": ["pipeline.ini"],
    },
    entry_points={
        "console_scripts": ["stravapipeline=strava_pipeline.main:main"],
    },
)
