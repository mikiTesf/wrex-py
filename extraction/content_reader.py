from typing import List
from zipfile import ZipFile

from extraction.pub_extract import PubExtract


class ContentReader:

    def __init__(self):
        self.__UNNEEDED_CONTENT_NAMES = [
            'OEBPS/images',
            'OEBPS/css',
            'OEBPS/pagenav',  # a number follows after 'pagenav'
            'OEBPS/content.opf',
            'OEBPS/cover.xhtml',
            'OEBPS/toc.ncx',
            'OEBPS/toc.xhtml',
            'META-INF',
            'mimetype',
            'extracted'
        ]

    def get_publication_extracts(self, pub_files):
        pub_extracts = []  # type: List[PubExtract]
        print('reading publication content...')

        for mwb_pub in pub_files:
            meeting_extracts = []
            epub_archive = ZipFile(mwb_pub)

            for entry_name in epub_archive.namelist():
                if self._unneeded_entry(entry_name):
                    continue

                content_string = epub_archive.read(entry_name).decode('utf-8')
                if not self._unneeded_xhtml(content_string):
                    continue
                meeting_extracts.append(content_string)
            epub_archive.close()
            pub_extracts.append(PubExtract(mwb_pub.name, meeting_extracts))

        return pub_extracts

    def _unneeded_entry(self, entry_name):
        for test_name in self.__UNNEEDED_CONTENT_NAMES:
            if test_name in entry_name:
                return True
        return False

    def _unneeded_xhtml(self, content_string):
        treasures_exists = 'shadedHeader treasures' in content_string
        ministry_exists = 'shadedHeader ministry' in content_string
        christian_living_exists = 'shadedHeader christianLiving' in content_string

        return treasures_exists and ministry_exists and christian_living_exists
