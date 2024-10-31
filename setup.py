from setuptools import setup, find_packages

setup(
    name="sinAPI",
    version="0.2.0",
    author="sinortax",
    description="Интерфейс связи ботов Tegtory с апи",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sheptalo/my_sin_api",
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
