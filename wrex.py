from extraction.content_reader import ContentReader
from extraction.content_parser import ContentParser
from excel.excel_doc_generator import ExcelGenerator

import json
import sys
import collections
import re

content_reader = ContentReader()
HELP = """
NAME
        wrex-py (from the original wrex written in Java)

SYNOPSIS
        python3 wrex.py [-v|--version] [-h|--help] [<paths>]

DESCRIPTION
        Extracts the presentations in an MWB (Meeting Workbook) publication and prepares an Excel document
        making assignments easy for the responsible Elder or Ministerial Servant. It is mandatory that all
        files passed to WREX be in the EPUB format.

OPTIONS
        -h, --help
            Display this help and exit.

        -v, --version
            Show version information and exit.
"""
VERSION = 'v0.1'

options = []
file_args = []

raw_arguments = collections.deque(sys.argv[1:])

if len(raw_arguments) == 0:
    print(HELP)
    sys.exit()

while len(raw_arguments) != 0:
    arg = raw_arguments.popleft()

    if arg in ['-h', '--help']:
        print(HELP)
        sys.exit()
    if arg in ['-v', '--version']:
        print(VERSION)
        sys.exit()

    try:
        file_args.append(open(arg, mode='rb'))
    except FileNotFoundError:
        print(HELP)
        sys.exit()

pub_extracts = content_reader.get_publication_extracts(file_args)

with open('language/english.json', mode='r') as language_file:
    language_pack = json.load(language_file)

content_parser = ContentParser(pub_extracts, language_pack['filter_for_minute'])
pub_extracts = content_parser.build_meeting_objects()

excel_generator = ExcelGenerator(pub_extracts, language_pack)
excel_generator.create_excel_doc()
