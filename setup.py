import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binance-transaction",
    version="0.0.3",
    author="William Morriss",
    author_email="wjmelements@gmail.com",
    description="Binance Chain Transactions",
    install_requires=['ecdsa'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trusttoken/bnb-tx-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
