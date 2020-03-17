from extraction.content_reader import ContentReader
from extraction.content_parser import ContentParser
from excel.generate_excel_doc import ExcelGenerator

import json

content_reader = ContentReader()
epub_files = ["sample_mwbs/mwb_E_202004.epub"]

meeting_content = content_reader.get_meeting_files(epub_files)

language_file = open('language/english.json')
language_pack = json.load(language_file)

content_parser = ContentParser(meeting_content, language_pack['filter_for_minute'])
meetings = content_parser.build_meeting_objects()

excel_generator = ExcelGenerator(meetings, language_pack)
excel_generator.create_excel_doc()
