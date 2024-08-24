from setuptools import setup, find_packages

def get_requirements(file_path: str):
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements

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
    install_requires=get_requirements('requirements.txt'),
)
