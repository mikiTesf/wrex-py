from typing import List

from bs4 import BeautifulSoup
import json
from os.path import join, dirname

from extraction.pub_extract import PubExtract
from meeting.meeting import Meeting
from meeting.section_kind import SectionKind
from meeting.meeting_section import MeetingSection


class ContentParser:

    def __init__(self, filter_for_minute: str = None):
        self.filter_for_minute = filter_for_minute

        with open(join(dirname(__file__), 'element_selectors.json'), 'r') as json_file:
            self.element_selectors = json.load(json_file)

    def build_meeting_objects(self, extract: dict):
        meetings: List[Meeting] = []

        for week_meeting_content in extract['string_extracts']:
            meeting_content = BeautifulSoup(week_meeting_content, 'html.parser')
            # the next few lines is where the meeting object is built
            week_span = meeting_content.find(self.element_selectors["week_span_element"]).get_text()
            treasures_section = self.get_section_content(SectionKind.TREASURES, meeting_content)
            ministry_section = self.get_section_content(SectionKind.IMPROVE_IN_MINISTRY, meeting_content)
            christian_section = self.get_section_content(SectionKind.CHRISTIAN_LIVING, meeting_content)

            meetings.append(Meeting(week_span, treasures_section, ministry_section, christian_section))

        return PubExtract(extract['file_name'], meetings)

    def get_section_content(self, section_kind, meeting_content):
        section_title = self.get_section_title(section_kind, meeting_content)
        meeting_section = MeetingSection(section_kind, section_title)
        section_presentations = self.get_section_presentations(section_kind, meeting_content)
        meeting_section.set_presentations(section_presentations)

        return meeting_section

    def get_section_title(self, section_kind: SectionKind, meeting_content: BeautifulSoup):
        if section_kind == SectionKind.TREASURES:
            title_element = meeting_content.find('div', id=self.element_selectors["treasures_section_id"])
            title_element = title_element.find(self.element_selectors["meeting_section_title_element"]).get_text()
        elif section_kind == SectionKind.IMPROVE_IN_MINISTRY:
            title_element = meeting_content.find('div', id=self.element_selectors["ministry_section_id"])
            title_element = title_element.find(self.element_selectors["meeting_section_title_element"]).get_text()
        else:
            title_element = meeting_content.find('div', id=self.element_selectors["christian_life_section_id"])
            title_element = title_element.find(self.element_selectors["meeting_section_title_element"]).get_text()

        return title_element

    def get_section_presentations(self, section_kind: SectionKind, meeting_content: BeautifulSoup):
        section_dom = self.get_section_dom(section_kind, meeting_content)
        presentations = []
        section_dom = section_dom.find_all(self.element_selectors["presentation_element"])

        if section_kind == SectionKind.CHRISTIAN_LIVING:
            del section_dom[0]  # transition song
            del section_dom[-2:]  # "concluding song" and "next week preview"

        for li in section_dom:
            presentation_content = li.find_next(self.element_selectors["presentation_titles_element"]).get_text()

            if self.filter_for_minute not in presentation_content:
                continue
            presentation_content = presentation_content[0:presentation_content.index(self.filter_for_minute)]
            presentation_content = presentation_content + self.filter_for_minute + ')'
            presentations.append(presentation_content)

        return presentations

    def get_section_dom(self, section_kind: SectionKind, meeting_content: BeautifulSoup):
        if section_kind == SectionKind.TREASURES:
            section_dom = meeting_content.find('div', id=self.element_selectors["treasures_section_id"])
        elif section_kind == SectionKind.IMPROVE_IN_MINISTRY:
            section_dom = meeting_content.find('div', id=self.element_selectors["ministry_section_id"])
        else:  # section_kind equals SectionKind.CHRISTIAN_LIVING
            section_dom = meeting_content.find('div', id=self.element_selectors["christian_life_section_id"])

        section_dom = section_dom.find_next('div').find_next(self.element_selectors["presentations_group_selector"])
        return section_dom
