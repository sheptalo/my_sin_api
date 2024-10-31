from setuptools import setup, find_packages

setup(
    name="sinAPI",
    version="0.1.0",
    author="sinortax",
    description="Интерфейс связи ботов Tegtory с апи",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/XakepAnonim/structure_generator",
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0",
        "python-dotenv>=0.19.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)