import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Manzur utils", # Replace with your own username
    version="0.0.1",
    author="Hazem AL SAIED",
    author_email="hazemalsaied@gmail.com",
    description="A library of functions/ modules for data analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hazemalsaied/manzur",
    project_urls={
        "Bug Tracker": "https://github.com/hazemalsaied/manzur/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)