from typing import List
import re

from meeting.meeting import Meeting


class PubExtract:

    def __init__(self, pub_name: str, meetings: List[Meeting]):
        self.pub_name = pub_name
        self.meetings = meetings
        self._format_pub_name()
        self.pub_year_and_month = self.pub_name[self.pub_name.rfind('_') + 1:]
        self.pub_month = self._get_pub_month()
        self.pub_year = self._get_pub_year()

    def _get_pub_month(self):
        month_digits = self.pub_year_and_month[-2:]  # the last 2 digits represent the publication's month
        return month_digits

    def _get_pub_year(self):
        year_digits = self.pub_year_and_month[:4]  # the first 4 digits represent the publication's year
        return year_digits

    def _format_pub_name(self):
        self.pub_name = re.sub(r'\.epub', '', self.pub_name)
        index_of_last_mwb = self.pub_name.rfind('mwb')
        self.pub_name = self.pub_name[index_of_last_mwb:]
