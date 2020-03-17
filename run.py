from extraction.content_reader import ContentReader
from extraction.content_parser import ContentParser
from excel.generate_excel_doc import ExcelGenerator

extractor = ContentReader()
epub_files = ["sample_mwbs/mwb_E_202004.epub"]

meeting_content = extractor.get_meeting_files(epub_files)

meeting_builder = ContentParser(meeting_content)
meetings = meeting_builder.build_meeting_objects()

excel_generator = ExcelGenerator(meetings)
excel_generator.create_excel_doc()
# for meeting in meetings:
#     print(meeting._week_span)
#
#     for presentation in meeting._treasures_section.presentations:
#         print(presentation)
#
#     for presentation in meeting._ministry_section.presentations:
#         print(presentation)
#
#     for presentation in meeting._christian_section.presentations:
#         print(presentation)
