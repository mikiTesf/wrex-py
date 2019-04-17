class MeetingSection:

    def __init__(self, section_kind, title, presentations):
        self.__section_kind = section_kind
        self.__title = title
        # self.__presentations is a `list` of presentations under the section
        self.__presentations = presentations
