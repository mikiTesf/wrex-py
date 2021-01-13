from os import environ
from os.path import join


CONFIG_DIR_PATH = join(environ.get('HOME'), '.wrex-py')
LANGUAGES_DIR_NAME = 'language'
LANGUAGES_DIR_PATH = join(CONFIG_DIR_PATH, LANGUAGES_DIR_NAME)
