import setuptools
import importlib.util

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="pywalletconnectv1",
    version= "0.1.1",
    author="Toporin",
    author_email="satochip.wallet@gmail.com",
    description="Simple python library that implements WalletConnect protocol v1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Toporin/pywalletconnectv1",
    project_urls={
        'Github': 'https://github.com/Toporin',
        'Webshop': 'https://satochip.io/',
        'Telegram': 'https://t.me/Satochip',
        'Twitter': 'https://twitter.com/satochipwallet',
        'Source': 'https://github.com/Toporin/pywalletconnectv1/',
        'Tracker': 'https://github.com/Toporin/pywalletconnectv1/issues',
    },
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
