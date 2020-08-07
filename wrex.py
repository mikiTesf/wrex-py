from extraction.content_reader import ContentReader
from extraction.content_parser import ContentParser
from excel.excel_doc_generator import ExcelGenerator

import json, sys, collections
from os import sep


content_reader = ContentReader()
VERSION = 'v0.1'
LANGUAGE_FOLDER = 'language' + sep

try:
    with open('HELP', 'r') as help_file:
        HELP = help_file.read()
except FileNotFoundError:
    HELP = 'Help file is missing. Please read the documentation at https://www.github.com/mikiTesf/wrex-py'

try:
    lang_resolver_path = LANGUAGE_FOLDER + 'lang_code.json'
    with open(lang_resolver_path, mode='r') as lang_resolver:
        LANG_CODE_PAIR = json.load(lang_resolver)
except FileNotFoundError:
    print(lang_resolver_path, 'missing. Exiting...')
    sys.exit()


def get_lang_code(pub_name):
    last_file_separator_index = pub_name.find(sep)
    pub_name = pub_name[last_file_separator_index + 1:]
    first_underscore_index = pub_name.find('_')
    second_underscore_index = pub_name.find('_', first_underscore_index + 1)
    return pub_name[first_underscore_index + 1:second_underscore_index]


def get_lang_pack(lang_code='E'):
    lang_pack_name = LANG_CODE_PAIR[lang_code] + '.json'
    lang_pack = open(LANGUAGE_FOLDER + lang_pack_name, mode='r')
    return json.load(lang_pack)


options = []
file_args = []

raw_arguments = collections.deque(sys.argv[1:])

if len(raw_arguments) == 0:
    print(HELP)
    sys.exit()

while len(raw_arguments) != 0:
    arg = raw_arguments.popleft()

    if len(file_args) == 0:
        if arg in ['-h', '--help']:
            print(HELP)
            sys.exit()
        if arg in ['-v', '--version']:
            print(VERSION)
            sys.exit()

    try:
        file_args.append(open(arg, mode='rb'))
    except (FileNotFoundError, IsADirectoryError):
        print(HELP)
        sys.exit()


lang_pub_pair = {}

for pub_file in file_args:
    lang_code = get_lang_code(pub_file.name)

    if lang_pub_pair.get(lang_code) is None:
        lang_pub_pair[lang_code] = [pub_file]
    else:
        lang_pub_pair[lang_code].append(pub_file)

content_parser = ContentParser()

for lang_key in lang_pub_pair:
    language_pack = get_lang_pack(lang_code=lang_key)
    pub_extracts = content_reader.get_publication_extracts(lang_pub_pair[lang_key])
    content_parser.entire_publication_extracts = pub_extracts
    content_parser.filter_for_minute = language_pack['filter_for_minute']
    pub_extracts = content_parser.build_meeting_objects()

    excel_generator = ExcelGenerator(pub_extracts, language_pack)
    excel_generator.create_excel_doc()
