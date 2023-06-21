from setuptools import find_packages, setup

setup(
    name="strava_pipeline",
    version="0.1",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": [
            "stravapipeline=strava_pipeline.main:main",
        ],
    },
)
