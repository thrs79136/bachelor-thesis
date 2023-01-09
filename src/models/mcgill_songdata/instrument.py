from typing import re

from src.models.mcgill_songdata.instrument_type import InstrumentType


class Instrument:
    def __init__(self, name):

        self.name = re.sub('[(),]', '', name)

        opening_brace = '(' in name
        closing_brace = ')' in name
        if opening_brace and not closing_brace:
            self.instrumentType = InstrumentType.BEGINNING
        elif not opening_brace and closing_brace:
            self.instrumentType = InstrumentType.END
        else:
            self.instrumentType = InstrumentType.SECTION
