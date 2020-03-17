from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from typing import List
from meeting.meeting import Meeting
from meeting.meeting_section import MeetingSection
from meeting.section_kind import SectionKind


class ExcelGenerator(object):

    def __init__(self, meeting_objects: List[List[Meeting]]):
        self.workbook = Workbook()
        self.meeting_object_lists = meeting_objects
        self.__CURRENT_ROW = 3
        self.__LEFT_COLUMNS = ['B', 'C', 'D', 'E']
        self.__RIGHT_COLUMNS = ['G', 'H', 'I', 'J']
        self.__ACTIVE_COLUMNS = self.__LEFT_COLUMNS
        # a new sheet is created for each publication so the program won't
        # use the first sheet (it will be empty). Hence, it it removed
        self.workbook.remove_sheet(worksheet=self.workbook.get_active_sheet())

    def create_excel_doc(self):
        print('creating excel document...')

        for meeting_object_list in self.meeting_object_lists:
            self._add_populated_sheet(meeting_object_list)

        self.workbook.save('wrex.xlsx')
        print('done...')

    def _add_populated_sheet(self, meeting_objects: List[Meeting]):
        sheet = self.workbook.create_sheet('pub')  # todo: change with publication `file name`
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
                self.__CURRENT_ROW = 5
                self.__ACTIVE_COLUMNS = self.__RIGHT_COLUMNS
        # reset indexes and make them ready for the next sheet
        self.__CURRENT_ROW = 3
        self.__ACTIVE_COLUMNS = self.__LEFT_COLUMNS

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

    def _insert_header_content(self, week_span: str, sheet: Worksheet):
        # week span
        current_row = str(self.__CURRENT_ROW)
        start_cell = self.__ACTIVE_COLUMNS[0] + current_row
        end_cell = self.__ACTIVE_COLUMNS[2] + current_row
        sheet[start_cell] = week_span  # todo: get month name from config file
        sheet.merge_cells(start_cell + ':' + end_cell)
        self.__CURRENT_ROW += 1
        # chairman
        current_row = str(self.__CURRENT_ROW)
        start_cell = self.__ACTIVE_COLUMNS[0] + current_row
        end_cell = self.__ACTIVE_COLUMNS[2] + current_row
        sheet[start_cell] = 'Chairman'  # todo: get equivalent from config file
        sheet.merge_cells(start_cell + ':' + end_cell)
        self.__CURRENT_ROW += 1
        # opening prayer
        current_row = str(self.__CURRENT_ROW)
        start_cell = self.__ACTIVE_COLUMNS[2] + current_row
        sheet[start_cell] = 'Opening Prayer'  # todo: get equivalent from config file
        self.__CURRENT_ROW += 1
        self._style_header_content()

    def _style_header_content(self):
        pass

    def _insert_section_title(self, meeting_section: MeetingSection, sheet: Worksheet):
        current_row = str(self.__CURRENT_ROW)
        start_cell = self.__ACTIVE_COLUMNS[0] + current_row
        sheet[start_cell] = meeting_section.title

        if meeting_section.section_kind == SectionKind.IMPROVE_IN_MINISTRY:
            end_cell = self.__ACTIVE_COLUMNS[1] + current_row
            self._insert_hall_divider(sheet)
        else:
            end_cell = self.__ACTIVE_COLUMNS[3] + current_row
        sheet.merge_cells(start_cell + ':' + end_cell)
        self.__CURRENT_ROW += 1
        self._style_section_title()

    def _style_section_title(self):
        pass

    def _insert_hall_divider(self, sheet):
        current_row = str(self.__CURRENT_ROW)
        main_hall_cell = self.__ACTIVE_COLUMNS[2] + current_row
        second_hall_cell = self.__ACTIVE_COLUMNS[3] + current_row
        sheet[main_hall_cell] = 'Main Hall'  # todo: get value from config file
        sheet[second_hall_cell] = 'Second Hall'  # todo: get value from config file

    def style_hall_divider(self, sheet):
        pass

    def _insert_section(self, meeting_section: MeetingSection, sheet: Worksheet):
        self._insert_section_title(meeting_section, sheet)
        bible_reading = 'Bible Reading:'  # todo: get value from config file

        for presentation in meeting_section.presentations:
            if meeting_section.section_kind == SectionKind.TREASURES:
                if bible_reading in presentation:
                    self._insert_hall_divider(sheet)
                    self.__CURRENT_ROW += 1
            current_row = str(self.__CURRENT_ROW)
            start_cell = self.__ACTIVE_COLUMNS[1] + current_row
            end_cell = self.__ACTIVE_COLUMNS[2] + current_row
            sheet[start_cell] = presentation
            if bible_reading not in presentation:
                sheet.merge_cells(start_cell + ':' + end_cell)
            self.__CURRENT_ROW += 1

        self._style_section()

    def _style_section(self):
        pass

    def _insert_footer_content(self, sheet: Worksheet):  # todo: get values from config file
        current_row = str(self.__CURRENT_ROW)
        cell = self.__ACTIVE_COLUMNS[2] + current_row
        sheet[cell] = 'Reader'
        self.__CURRENT_ROW += 1

        current_row = str(self.__CURRENT_ROW)
        cell = self.__ACTIVE_COLUMNS[2] + current_row
        sheet[cell] = 'Concluding Prayer'
        self.__CURRENT_ROW += 3

        self._style_footer_content()

    def _style_footer_content(self):
        pass
