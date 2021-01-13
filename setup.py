import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wrex-py",
    version="0.1",
    author="Mikyas Tesfamichael",
    author_email="mickyastesfamichael@gmail.com",
    description="Prepare Excel documents for mid-week meeting part assignments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikiTesf/wrex-py",
    packages=setuptools.find_packages(),
    install_requires=[
        "beautifulsoup4==4.8.2", "configparser==4.0.2",
        "et-xmlfile==1.0.1", "jdcal==1.4.1",
        "openpyxl==2.6.4", "soupsieve==2.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'wrex-py = wrex.__main__:main'
        ]
    },
    python_requires='>=3.6'
)
