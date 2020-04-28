from extraction.content_reader import ContentReader
from extraction.content_parser import ContentParser
from excel.excel_doc_generator import ExcelGenerator

import json
import sys

content_reader = ContentReader()
# "sample_mwbs/mwb_E_201909.epub", "sample_mwbs/mwb_E_202001.epub", "sample_mwbs/mwb_E_202004.epub"
# "sample_mwbs/mwb_TI_201904.epub"
# "sample_mwbs/mwb_AM_201904.epub", "sample_mwbs/mwb_AM_201905.epub"
# "sample_mwbs/mwb_F_201912.epub"

# parse options and arguments from sys.argv

options = []
arguments = []

for string in sys.argv[1:]:
    if string[0:2] == '--':
        options.append(string)
    else:
        arguments.append(string)

if '--help' in options:
    print('WREX-PY: The Python version of WREX! This is such a cool application!')
    sys.exit()
elif '--version' in options:
    print('v0.1 [build 1053]')
    sys.exit()

if len(arguments) == 0:
    print('No publications passed. Exiting...')
    sys.exit()

file_paths = arguments

epub_files = []

for file_path in sorted(file_paths):
    epub_files.append(open(file_path, mode='rb'))

pub_extracts = content_reader.get_publication_extracts(epub_files)

with open('language/english.json', mode='r') as language_file:
    language_pack = json.load(language_file)

content_parser = ContentParser(pub_extracts, language_pack['filter_for_minute'])
pub_extracts = content_parser.build_meeting_objects()

excel_generator = ExcelGenerator(pub_extracts, language_pack)
excel_generator.create_excel_doc()
