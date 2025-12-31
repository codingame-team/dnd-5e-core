from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dnd-5e-core",
    version="0.1.0",
    author="D&D Development Team",
    author_email="",
    description="Complete D&D 5th Edition Rules Engine - Core Game Logic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codingame-team/dnd-5e-core",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Framework :: D&D 5th Edition",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.20.0",
        "requests>=2.28.0",  # For D&D 5e API
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "mypy>=0.950",
            "flake8>=4.0",
            "requests-mock>=1.9.3",
        ],
    },
)
