from typing import List
import re

from wrex.meeting.meeting import Meeting


class PubExtract:

    def __init__(self, pub_name: str, meetings: List[Meeting]):
        self.pub_name = pub_name
        self.meetings = meetings
        match = re.search('(\\d{4})(\\d{2})', self.pub_name)
        self.pub_month = match.group(2)
        self.pub_year = match.group(1)
