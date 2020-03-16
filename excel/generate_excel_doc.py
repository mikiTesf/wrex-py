from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from typing import List
from meeting.meeting import Meeting
from meeting.meeting_section import MeetingSection


class ExcelGenerator(object):

    def __init__(self, meeting_objects: List[List[Meeting]]):
        self.workbook = Workbook()
        self.list_of_meeting_objects = meeting_objects
        self.__CURRENT_ROW = 3
        self.__LEFT_COLUMNS = ['B', 'C', 'D', 'E']
        self.__RIGHT_COLUMNS = ['G', 'H', 'I', 'J']

    def create_excel_doc(self):
        print('creating excel document...')
        for meeting_objects in self.list_of_meeting_objects:  # type: List[Meeting]
            sheet = self.workbook.create_sheet('name_me_nigga')  # todo: change with publication `file name`
            meetings_count = 0

            self._insert_sheet_title(sheet)
            for meeting in meeting_objects:
                self._insert_header_content(meeting.week_span, sheet)
                self._insert_section(meeting.treasures_section, sheet)
                self._insert_section(meeting.ministry_section, sheet)
                self._insert_section(meeting.christian_section, sheet)
                self._insert_footer_content(sheet)

                meetings_count += 1
                if meetings_count == 3:
                    self.__CURRENT_ROW = 3

        self.workbook.save('dreadlocks.xlsx')
        print('done...')

    def _insert_sheet_title(self, sheet: Worksheet):
        current_row = str(self.__CURRENT_ROW)
        start_cell = self.__LEFT_COLUMNS[0] + str(current_row)
        end_cell = self.__RIGHT_COLUMNS[3] + str(current_row)
        sheet[start_cell] = 'Christian Life And Ministry'  # todo: get value from config file
        sheet.merge_cells(start_cell + ':' + end_cell)
        self.__CURRENT_ROW += 2
        self._style_sheet_title()

    def _style_sheet_title(self):
        pass

    def _insert_header_content(self, week_span: str, sheet: Worksheet):  # todo: get month names from config file
        start_cell = self.__LEFT_COLUMNS[0] + str(self.__CURRENT_ROW)
        end_cell = self.__LEFT_COLUMNS[2] + str(self.__CURRENT_ROW)
        sheet[start_cell] = week_span
        sheet.merge_cells(start_cell, end_cell)
        self.__CURRENT_ROW += 1
        # bla bla bla
        self._style_header_content()

    def _style_header_content(self):
        pass

    def _insert_section_title(self, sheet: Worksheet):
        self._style_section_title()
        pass

    def _style_section_title(self):
        pass

    def _insert_section(self, meeting_section: MeetingSection, sheet: Worksheet):
        # todo: get values from config file
        self._insert_section_title(sheet)
        self._style_section()
        pass

    def _style_section(self):
        pass

    def _insert_footer_content(self, sheet: Worksheet):  # todo: get values from config file
        self._style_footer_content()
        pass

    def _style_footer_content(self):
        pass
