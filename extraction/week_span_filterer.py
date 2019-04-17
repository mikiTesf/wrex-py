class WeekSpanFilterer:

    @staticmethod
    def filter(pub_extracts):
        meeting_files_set = []

        for meeting_files in pub_extracts:
            filtered_meeting_files = []

            for meeting_file in meeting_files:
                dom = meeting_file.read().decode('utf-8')

                treasures_exists = 'shadedHeader treasures' in dom
                ministry_exists = 'shadedHeader ministry' in dom
                christian_living_exists = 'shadedHeader christianLiving' in dom

                if treasures_exists and ministry_exists and christian_living_exists:
                    filtered_meeting_files.append(meeting_file)

            meeting_files_set.append(filtered_meeting_files)

        return meeting_files_set
