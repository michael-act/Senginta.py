import setuptools

LIST_PACKAGES = ['senginta', 'senginta.static', 'senginta.static.Baidu', 'senginta.static.Google']

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="senginta",                        # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Michael Abraham Chan Tulenan",  # Full name of the author
    author_email="michael.4ct@gmail.com", 
    description="All in one Search Engine for used by API or Python Module (Unofficial)",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=LIST_PACKAGES,                 # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    py_modules=["senginta"],                # Name of the python package
    install_requires=['beautifulsoup4']     # Install other dependencies if any
)