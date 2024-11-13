from setuptools import setup, find_packages

setup(
    name="wxled",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "gpiozero>=2.0",
        "python-dotenv>=1.0.0",
        "RPi.GPIO>=0.7.1",
    ],
    python_requires=">=3.8",
)