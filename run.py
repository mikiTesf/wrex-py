from extraction.content_reader import ContentReader
from extraction.content_parser import ContentParser
from excel.generate_excel_doc import ExcelGenerator

import json

content_reader = ContentReader()
# "sample_mwbs/mwb_E_201909.epub", "sample_mwbs/mwb_E_202001.epub", "sample_mwbs/mwb_E_202004.epub"
# "sample_mwbs/mwb_TI_201904.epub"
# "sample_mwbs/mwb_AM_201904.epub", "sample_mwbs/mwb_AM_201905.epub"
# "sample_mwbs/mwb_F_201912.epub"
file_paths = ["sample_mwbs/mwb_E_201909.epub", "sample_mwbs/mwb_E_202001.epub", "sample_mwbs/mwb_E_202004.epub"]
epub_files = []

for file_path in file_paths:
    epub_files.append(open(file_path, mode='rb'))

pub_extracts = content_reader.get_publication_extracts(epub_files)

with open('language/english.json', mode='r') as language_file:
    language_pack = json.load(language_file)

content_parser = ContentParser(pub_extracts, language_pack['filter_for_minute'])
pub_extracts = content_parser.build_meeting_objects()

excel_generator = ExcelGenerator(pub_extracts, language_pack)
excel_generator.create_excel_doc()
