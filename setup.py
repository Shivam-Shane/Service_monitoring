from setuptools import setup, find_packages

setup(
    name="gmail_monitoring",
    version="1.0.1",
    packages=find_packages(),
    author="SHIVAM",
    author_email="sk0551460@gmail.com",
    description="A package for monitoring Gmail messages, and works as per standard", 
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Shivam-Shane/gmail_monitoring..git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ::  GNU GENERAL PUBLIC LICENSE",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.3',
)
