# import re
from typing import List

from bs4 import BeautifulSoup

from meeting.meeting import Meeting
from meeting.section_kind import SectionKind
from meeting.meeting_section import MeetingSection


class MeetingBuilder:

    def __init__(self, entire_publication_extracts):
        self.entire_publication_extracts = entire_publication_extracts

    def build_meeting_objects(self):
        meetings = []  # type: List[Meeting]
        for single_publication_files in self.entire_publication_extracts:
            for week_meeting in single_publication_files:
                meeting_content = BeautifulSoup(week_meeting, 'html.parser')
                # the next few lines is where the meeting object is built
                week_span = meeting_content.find('title').text
                treasures_section = self.get_section_content(SectionKind.TREASURES, meeting_content)
                ministry_section = self.get_section_content(SectionKind.IMPROVE_IN_MINISTRY, meeting_content)
                christian_section = self.get_section_content(SectionKind.CHRISTIAN_LIVING, meeting_content)

                meetings.append(Meeting(
                    week_span,
                    treasures_section,
                    ministry_section,
                    christian_section
                ))

    def get_section_content(self, section_kind, meeting_content):
        section_title = self.get_section_title(section_kind, meeting_content)
        # the first 2 lines of code surely indicate to bad design (the MeetingSection)
        # object must be able to be declared without fetching the section's title first
        meeting_section = MeetingSection(section_kind, section_title)
        section_presentations = self.get_section_presentations(section_kind, meeting_content)
        meeting_section.set_presentations(section_presentations)

        return meeting_section

    def get_section_title(self, section_kind: SectionKind, meeting_content: BeautifulSoup):
        if section_kind == SectionKind.TREASURES:
            title = meeting_content.find('div', id='section2')
            title = title.find('h2', class_='shadedHeader treasures').text
        elif section_kind == SectionKind.IMPROVE_IN_MINISTRY:
            title = meeting_content.find('div', id='section3')
            title = title.find('h2', class_='shadedHeader ministry').text
        else:
            title = meeting_content.find('div', id='section4')
            title = title.find('h2', class_='shadedHeader christianLiving').text

        return title

    def get_section_presentations(self, section_kind: SectionKind, meeting_content: BeautifulSoup):
        section_dom = self.get_section_dom(section_kind, meeting_content)
        presentations = []
        filter_for_minute = ' min.'  # ደቂቃ section_dom.find_next('li').find_next('p').text.find('</strong>(

        for li in section_dom.find_all('li'):
            presentation_content = li.find_next('p').text

            if filter_for_minute not in presentation_content:
                continue
            presentation_content = presentation_content[0:presentation_content.index(filter_for_minute)]
            presentation_content = presentation_content + filter_for_minute + ')'
            presentations.append(presentation_content)

        return presentations

    def get_section_dom(self, section_kind: SectionKind, meeting_content: BeautifulSoup):
        if section_kind == SectionKind.TREASURES:
            section_dom = meeting_content.find('div', id='section2')
        elif section_kind == SectionKind.IMPROVE_IN_MINISTRY:
            section_dom = meeting_content.find('div', id='section3')
        else:  # section_kind equals SectionKind.CHRISTIAN_LIVING
            section_dom = meeting_content.find('div', id='section4')

        section_dom = section_dom.find_next('div').find_next('ul')
        return section_dom

