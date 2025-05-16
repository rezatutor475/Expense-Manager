from setuptools import setup, find_packages
import re


def get_version():
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    version_match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Version not found in main.py")


try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A professional expense management system built with FastAPI and Python."

setup(
    name="expense_manager",
    version=get_version(),
    description="A professional expense management system built with FastAPI and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Reza Torabi",
    author_email="rezatutor475@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi==0.95.0",
        "uvicorn[standard]==0.22.0",
        "mysql-connector-python==8.0.31",
        "pydantic==1.10.5",
        "pytest==7.2.0",
        "python-dotenv==0.21.0",
        "loguru==0.6.0",
        "httpx==0.23.0",
        "email-validator==1.3.1",
    ],
    entry_points={
        "console_scripts": [
            "expense-manager=main:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
