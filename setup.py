from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dxgridparser",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library to parse DevExpress ASPxGridView tables from BeautifulSoup objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dxgridparser",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "beautifulsoup4>=4.9.0",
        "pandas>=1.0.0",
    ],
)

