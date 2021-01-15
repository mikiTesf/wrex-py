from wrex.data.base_model import BaseModel

from peewee import CharField


class Language(BaseModel):
    # Language code (F, AM, PA, etc.)
    lang_key = CharField(max_length=50)
    # Text to put in the generated Excel document
    bible_reading = CharField(max_length=50)
    chairman = CharField(max_length=50)
    concluding_prayer = CharField(max_length=50)
    filter_for_minute = CharField(max_length=50)
    main_hall = CharField(max_length=50)
    meeting_name = CharField(max_length=50)
    opening_prayer = CharField(max_length=50)
    reader = CharField(max_length=50)
    second_hall = CharField(max_length=50)
    # Months (also to be put in the generated Excel doc)
    january = CharField(max_length=50)
    february = CharField(max_length=50)
    march = CharField(max_length=50)
    april = CharField(max_length=50)
    may = CharField(max_length=50)
    june = CharField(max_length=50)
    july = CharField(max_length=50)
    august = CharField(max_length=50)
    september = CharField(max_length=50)
    october = CharField(max_length=50)
    november = CharField(max_length=50)
    december = CharField(max_length=50)

    def get_month_name(self, month_num: str):
        if month_num == '01':
            return self.january
        elif month_num == '02':
            return self.february
        elif month_num == '03':
            return self.march
        elif month_num == '04':
            return self.april
        elif month_num == '05':
            return self.may
        elif month_num == '06':
            return self.june
        elif month_num == '07':
            return self.july
        elif month_num == '08':
            return self.august
        elif month_num == '09':
            return self.september
        elif month_num == '10':
            return self.october
        elif month_num == '11':
            return self.november
        elif month_num == '12':
            return self.december
        else:
            return 'NULL'

    def __str__(self):
        return self.lang_key
