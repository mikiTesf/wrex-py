from extraction.mwb_extractor import MWBExtractor
from extraction.meeting_builder import MeetingBuilder

extractor = MWBExtractor()
epub_files = ["sample_mwbs/mwb_E_202004.epub"]

meeting_files = extractor.get_meeting_files(epub_files)

meeting_builder = MeetingBuilder(meeting_files)
meetings = meeting_builder.build_meeting_objects()

for meeting in meetings:
    print(meeting._week_span)

    for presentation in meeting._treasures_section.presentations:
        print(presentation)

    for presentation in meeting._ministry_section.presentations:
        print(presentation)

    for presentation in meeting._christian_section.presentations:
        print(presentation)
