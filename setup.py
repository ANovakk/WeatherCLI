from setuptools import setup, find_packages

setup(
    name="weather_cli",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["Click",
                      'requests'],
    entry_points={
        "console_scripts": [
            "weather=weather_cli.main:main",
        ],
    },
)