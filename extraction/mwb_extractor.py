from zipfile import ZipFile
from extraction.week_span_filterer import WeekSpanFilterer


class MWBExtractor:

    __UNNEEDED_CONTENT_NAMES = [
        'OEBPS/images',
        'OEBPS/css',
        'META-INF',
        'mimetype',
        'OEBPS/pagenav',  # a number follows after 'pagenav'
        'extracted',
        'OEBPS/content.opf',
        'OEBPS/cover.xhtml',
        'OEBPS/toc.ncx',
        'OEBPS/toc.xhtml'
    ]

    @staticmethod
    def get_meeting_files(pub_files):
        pub_extracts = []

        for epub_archive in pub_files:
            meeting_extracts = []
            mwb_pub = ZipFile(epub_archive, mode='r')

            for entry_name in mwb_pub.namelist():
                if MWBExtractor.unneeded_entry(entry_name):
                    continue
                meeting_extracts.append(mwb_pub.open(entry_name))
            pub_extracts.append(meeting_extracts)

        week_span_filterer = WeekSpanFilterer()
        return week_span_filterer.filter(pub_extracts)

    @staticmethod
    def unneeded_entry(entry_name):
        for test_name in MWBExtractor.__UNNEEDED_CONTENT_NAMES:
            if test_name in entry_name:
                return True
        return False
