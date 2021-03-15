"""METAR specific functionality"""

level = 30

flight_category_rgb = {
    'LIFR': (level, 0, level),  # magenta
    'IFR': (level, 0, 0), # red
    'MVFR': (0, 0, level), # blue
    'VFR': (0, level, 0), # green
    }

class Metar:
    def __init__(self, pixel):
        self.pixel = pixel

    def parse_response(self, metar: str):
        print('parseing metar')
        print(metar)

        station_id = metar[1]
        flight_category = metar[30]
        pixel = airport_pixel[station_id]

        color = flight_category_rgb[flight_category]