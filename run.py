from extraction.mwb_extractor import MWBExtractor
from extraction.meeting_builder import MeetingBuilder

extractor = MWBExtractor()
epub_files = ["sample_mwbs/mwb_AM_201904.epub", "sample_mwbs/mwb_AM_201905.epub"]

meeting_files = extractor.get_meeting_files(epub_files)

meeting_builder = MeetingBuilder(meeting_files)
meeting_builder.build_meeting_objects()
