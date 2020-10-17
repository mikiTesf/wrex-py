import argparse
import json
import sys
import re
from os.path import join, basename

from extraction.content_parser import ContentParser
from extraction.content_reader import ContentReader
from excel.excel_doc_generator import ExcelGenerator


class WREX:

    def __init__(self):
        self._LANGUAGE_FOLDER = 'language'
        self._LANG_CODE_PAIR = None

        try:
            lang_resolver_path = join(self._LANGUAGE_FOLDER, 'lang_code.json')
            with open(lang_resolver_path, mode='r') as lang_resolver:
                self._LANG_CODE_PAIR = json.load(lang_resolver)
        except FileNotFoundError:
            sys.exit('Could not load language resolver. Exiting...')

    def get_lang_pack(self, lang_code: str = 'AM'):
        lang_pack_name = self._LANG_CODE_PAIR[lang_code] + '.json'
        lang_pack = open(join(self._LANGUAGE_FOLDER, lang_pack_name), mode='r')
        return json.load(lang_pack)

    def read_pubs_and_generate_excel(self, file_args: list):
        lang_pub_pair = self.get_lang_pub_pair(file_args)

        for lang_key in lang_pub_pair:
            language_pack = self.get_lang_pack(lang_code=lang_key)
            # generate Excel document(s)
            excel_generator = ExcelGenerator(
                self.get_pub_extracts(lang_pub_pair[lang_key],
                                      language_pack['filter_for_minute']), language_pack)
            excel_generator.create_excel_doc()

    @staticmethod
    def get_pub_extracts(publications: list, filter_for_minute: str):
        content_reader = ContentReader()
        content_parser = ContentParser()

        print('reading file(s)...')
        extracts = []
        for pub_file in publications:
            extract = content_reader.get_publication_extracts(pub_file)
            if extract:
                extracts.append(extract)
        if len(extracts) == 0:
            sys.exit('Unable to extract meeting content from the publications provided. Exiting...')
        # parse contents
        content_parser.filter_for_minute = filter_for_minute
        print('parsing dom to build meeting objects...')
        pub_extracts = []
        for pub_extract in extracts:
            extract = content_parser.build_meeting_objects(pub_extract)
            if extract:
                pub_extracts.append(extract)

        return pub_extracts

    @staticmethod
    def get_lang_pub_pair(file_args: list):
        lang_pub_pair = {}

        for pub_file in file_args:
            match = re.match('^mwb_(\\w+)_\\d+.*$', basename(pub_file.name), re.IGNORECASE)

            if lang_pub_pair.get(match.group(1)) is None:
                lang_pub_pair[match.group(1)] = [pub_file]
            else:
                lang_pub_pair[match.group(1)].append(pub_file)
        return lang_pub_pair


if __name__ == '__main__':
    description = '''
    wrex-py (from the original wrex written in Java) extracts the presentations in a Meeting Workbook and
    prepares an Excel document making assignments easy for the responsible Elder or Ministerial Servant.
    It is mandatory that all files passed to wrex-py be in the EPUB format.'''

    arg_parser = argparse.ArgumentParser(
        prog='wrex-py',
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
        epilog='Give the Java version a try. Its faster!')

    arg_parser.version = 'version 0.1'
    arg_parser.add_argument('path', action='store',
                            help='path to a meeting workbook file(s)', nargs='+')
    arg_parser.add_argument('-v', '--version', action='version')

    parsed_args = arg_parser.parse_args()

    wrex = WREX()
    wrex.read_pubs_and_generate_excel(
        [open(pub, 'rb') for pub in parsed_args.path])
