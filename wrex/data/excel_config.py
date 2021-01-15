from wrex.data.base_model import BaseModel

from peewee import FloatField, IntegerField, CharField, BooleanField
from peewee import DoesNotExist


class ExcelConfig(BaseModel):
    # FONT SIZES #
    SHEET_TITLE_FONT_SIZE = IntegerField(default=18)
    # controls the font size of text such as labels (opening prayer, reader, ect.)
    # and hall dividing text (main hall, second hall) on a sheet
    SMALL_FONT_SIZE = IntegerField(default=15)
    # controls the font size of larger texts on a sheet such as week spans and
    # section titles
    LARGE_FONT_SIZE = IntegerField(default=16)
    # LENGTHS and HEIGHTS #
    MARGIN_LENGTH = FloatField(default=0.4)
    ROW_HEIGHT = IntegerField(default=25)
    # COLORS #
    TREASURES_SECTION_TITLE_BG_COLOR = CharField(default="5a6a70")
    MINISTRY_SECTION_TITLE_BG_COLOR = CharField(default="c18626")
    CHRISTIAN_LIFE_SECTION_TITLE_BG_COLOR = CharField(default="961526")
    DEFAULT_BG_COLOR = CharField(default='c8c8c8')
    # OTHERS #
    INSERT_HALL_DIVISION_LABELS = BooleanField(default=True)

    @staticmethod
    def get_default_config():
        default_config = ExcelConfig(
            id=1,
            SHEET_TITLE_FONT_SIZE=18,
            SMALL_FONT_SIZE=15,
            LARGE_FONT_SIZE=16,
            MARGIN_LENGTH=0.4,
            ROW_HEIGHT=25,
            TREASURES_SECTION_TITLE_BG_COLOR="5a6a70",
            MINISTRY_SECTION_TITLE_BG_COLOR="c18626",
            CHRISTIAN_LIFE_SECTION_TITLE_BG_COLOR="961526",
            DEFAULT_BG_COLOR='c8c8c8',
            INSERT_HALL_DIVISION_LABELS=True)
        default_config.create()
        return default_config

    @staticmethod
    def get_last_saved_settings():
        try:
            return ExcelConfig.get(id=1)
        except DoesNotExist:
            return ExcelConfig.get_default_config()

    class Meta:
        table_name = 'excel_config'
