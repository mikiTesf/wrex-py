from typing import List


class MeetingSection:

    def __init__(self, section_kind, title):
        self.section_kind = section_kind
        self.title = title
        self.presentations = None  # type: List[str]

    def set_presentations(self, presentations):
        self.presentations = presentations