"""
Setup script for XMLRiver Pro
"""
from setuptools import setup, find_packages
import os

# Читаем README для long_description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Professional Python client for XMLRiver API with full coverage"

setup(
    name="xmlriver-pro",
    version="1.2.2",
    author="XMLRiver Pro Team",
    author_email="support@xmlriver.com",
    description="Professional Python client for XMLRiver API with full coverage",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/xmlriver-pro/xmlriver-pro",
    project_urls={
        "Documentation": "https://xmlriver-pro.readthedocs.io/",
        "Bug Reports": "https://github.com/xmlriver-pro/xmlriver-pro/issues",
        "Source": "https://github.com/xmlriver-pro/xmlriver-pro",
        "Homepage": "https://xmlriver.com",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: XML",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
        "xmltodict>=0.13.0",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "pylint>=2.17.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "myst-parser>=1.0.0",
        ],
    },
    keywords=[
        "xmlriver",
        "google",
        "yandex",
        "search",
        "api",
        "seo",
        "scraping",
        "search-engine",
        "news",
        "images",
        "maps",
        "ads"
    ],
    include_package_data=True,
    zip_safe=False,
)
