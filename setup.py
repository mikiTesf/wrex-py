import setuptools
from setuptools.command.install import install
from os import makedirs, listdir
from os.path import join
from shutil import move

from wrex import constants


class CustomInstall(install):

    def run(self):
        # create directory to keep language files in
        makedirs(constants.CONFIG_DIR_PATH, exist_ok=True)
        print(f"putting language files in '{constants.LANGUAGES_DIR_PATH}'")
        # The reason why the absolute path of the 'language' folder is being used is
        # in order to replace the existing language files in case of a re-install. When
        # the relative path to the 'language' folder is used the installation fails with
        # '<path to language>...already exists'
        for lang_file in listdir(constants.LANGUAGES_DIR_NAME):
            move(join(constants.LANGUAGES_DIR_NAME, lang_file),
                 join(constants.CONFIG_DIR_PATH, constants.LANGUAGES_DIR_NAME, lang_file))

        install.run(self)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    cmdclass={
        'install': CustomInstall
    },
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
            'wrex-py = wrex.wrex:main'
        ]
    },
    python_requires='>=3.6'
)
