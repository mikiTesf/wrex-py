#!/usr/bin/env python

import argparse
import json
import sys
import re
from os.path import join, basename

from wrex.extraction.content_parser import ContentParser
from wrex.extraction.content_reader import ContentReader
from wrex.excel.excel_doc_generator import ExcelGenerator
from wrex.excel.config import ExcelConfig

from wrex.constants.constants import LANGUAGES_DIR_PATH


class WREX:

    def __init__(self):
        self._LANGUAGE_FOLDER = LANGUAGES_DIR_PATH
        self._LANG_CODE_PAIR = None

        # noinspection PyTypeChecker
        self.arg_parser = argparse.ArgumentParser(
            prog='wrex-py',
            description='''
    wrex-py (from the original wrex written in Java) extracts the presentations in a Meeting Workbook and
    prepares an Excel document making assignments easy for the responsible Elder or Ministerial Servant.
    It is mandatory that all files passed to wrex-py be in the EPUB format.''',
            formatter_class=argparse.RawTextHelpFormatter,
            allow_abbrev=False,
            epilog='Give the Java version a try. Its faster!')

        self.arg_parser.version = 'version 0.1'
        self.arg_parser.add_argument('path', action='store',
                                     help='path to a meeting workbook EPUB', nargs='+')
        self.arg_parser.add_argument('-s', '--single-hall', action='store_false',
                                     help='''don't insert hall dividing labels above presentation rows
        (bible reading and improve in ministry)''')
        self.arg_parser.add_argument('-v', '--version', action='version')

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

    def read_pubs_and_generate_excel(self, file_args: list, config: ExcelConfig):
        lang_pub_pair = self.get_lang_pub_pair(file_args)

        for lang_key in lang_pub_pair:
            language_pack = self.get_lang_pack(lang_code=lang_key)
            # generate Excel document(s)
            excel_generator = ExcelGenerator(
                self.get_pub_extracts(lang_pub_pair[lang_key], language_pack['filter_for_minute']),
                language_pack, config)
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
            sys.exit('Unable to extract meeting content from the publication(s) provided. Exiting...')
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
            file_name = basename(pub_file.name)
            match = re.match('^mwb_([A-Z]+)_\\d+.*$', file_name)

            if not match:
                print(f"'{file_name}': this file's name is inconvenient for processing.",
                      "Its name must follow: mwb_<LANG_CODE>_<YEAR-MONTH>.epub. Skipping...")
                continue

            if lang_pub_pair.get(match.group(1)) is None:
                lang_pub_pair[match.group(1)] = [pub_file]
            else:
                lang_pub_pair[match.group(1)].append(pub_file)
        return lang_pub_pair


def main():
    wrex = WREX()
    parsed_args = wrex.arg_parser.parse_args()
    excel_config = ExcelConfig()
    excel_config.INSERT_HALL_DIVISION_LABELS = parsed_args.single_hall

    paths = []

    for pub in parsed_args.path:
        try:
            paths.append(open(pub, 'rb'))
        except (IsADirectoryError, FileNotFoundError):
            print(f"'{pub}': this file is either a directory or it doesn't exist")

    wrex.read_pubs_and_generate_excel(paths, excel_config)


if __name__ == '__main__':
    sys.exit(main())
