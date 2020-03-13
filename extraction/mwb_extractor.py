from typing import List
from zipfile import ZipFile


class MWBExtractor:

    def __init__(self):
        self.__UNNEEDED_CONTENT_NAMES = [
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

    def get_meeting_files(self, pub_files):
        pub_extracts = []  # type: List[List[str]]

        for epub_archive in pub_files:
            meeting_extracts = []  # type: List[str]
            mwb_pub = ZipFile(epub_archive, mode='r')

            for entry_name in mwb_pub.namelist():
                if self.unneeded_entry(entry_name):
                    continue

                content_string = mwb_pub.read(entry_name).decode('utf-8')
                if not self.unneeded_xhtml(content_string):
                    continue
                meeting_extracts.append(content_string)
            pub_extracts.append(meeting_extracts)

        return pub_extracts

    def unneeded_entry(self, entry_name):
        for test_name in self.__UNNEEDED_CONTENT_NAMES:
            if test_name in entry_name:
                return True
        return False

    def unneeded_xhtml(self, content_string):
        treasures_exists = 'shadedHeader treasures' in content_string
        ministry_exists = 'shadedHeader ministry' in content_string
        christian_living_exists = 'shadedHeader christianLiving' in content_string

        return (treasures_exists and ministry_exists and christian_living_exists)
