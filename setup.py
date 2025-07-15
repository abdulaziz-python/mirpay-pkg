# MirPay Python paketini o'rnatish uchun sozlash fayli
from setuptools import setup, find_packages

setup(
    name="mirpay",
    version="1.5.0",
    author="Sizning Ismingiz",
    author_email="sizning.email@example.com",
    description="MirPay to'lov API uchun professional Python klienti",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sizningusername/mirpay-python",
    packages=find_packages(),
    install_requires=["requests>=2.28.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.7",
)
