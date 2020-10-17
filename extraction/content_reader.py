from os.path import basename

from zipfile import ZipFile
from zipfile import BadZipFile


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

    def get_publication_extracts(self, pub_file):
        meeting_extracts = []

        try:
            epub_archive = ZipFile(pub_file)
        except BadZipFile:
            print('"{}" is not an EPUB file. Skipping...'.format(pub_file.name))
            return

        for entry_name in epub_archive.namelist():
            if not self._unneeded_entry(entry_name):
                content_string = epub_archive.read(entry_name).decode('utf-8')
                if self._is_a_meeting_xhtml(content_string):
                    meeting_extracts.append(content_string)
        epub_archive.close()

        return {'file_name': basename(pub_file.name).replace('.epub', ''), 'string_extracts': meeting_extracts}

    def _unneeded_entry(self, entry_name):
        for test_name in self.__UNNEEDED_CONTENT_NAMES:
            if test_name in entry_name:
                return True
        return False

    @staticmethod
    def _is_a_meeting_xhtml(content_string):
        treasures_exists = 'shadedHeader treasures' in content_string
        ministry_exists = 'shadedHeader ministry' in content_string
        christian_living_exists = 'shadedHeader christianLiving' in content_string

        return treasures_exists and ministry_exists and christian_living_exists
