from setuptools import setup, find_packages

setup(
    name="token-tail",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click>=7.0", "tiktoken>=0.2.0"],
    entry_points={
        "console_scripts": [
            "token-tail=token_tail.main:cli",
        ],
    },
)
