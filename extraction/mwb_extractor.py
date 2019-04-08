from zipfile import ZipFile


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
    def get_meeting_files():
        # '../sample_mwbs/mwb_AM_201904.epub' is used as a test-file
        # to check class functionality
        mwb_pub = ZipFile('../sample_mwbs/mwb_AM_201904.epub', mode='r')
        meeting_files = []

        for entry_name in mwb_pub.namelist():
            if MWBExtractor.unneeded_entry(entry_name):
                continue
            meeting_files.append(mwb_pub.open(entry_name))

        # for file_ in meeting_files:
        #     print(file_.name)
        return meeting_files

    @staticmethod
    def unneeded_entry(entry_name):
        for test_name in MWBExtractor.__UNNEEDED_CONTENT_NAMES:
            if test_name in entry_name:
                return True
        return False
