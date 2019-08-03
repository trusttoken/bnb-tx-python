import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bnb-tx",
    version="0.0.4",
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
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
