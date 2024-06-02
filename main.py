""" Neopixel METAR map """

# connect to wifi
import secrets

from config import neopixel_pin, airport_pixel
import machine
import neopixel
import time
import urequests as requests
import utime
import math

# It's useful to test a longer strip periodically, so just init to 100
# lights = max(airport_pixel.values()) +1
lights = 100

np = neopixel.NeoPixel(machine.Pin(neopixel_pin), lights)
airport_metar = {}

level = 30

flight_category_rgb = {
    "LIFR": (level, 0, level),  # magenta
    "IFR": (level, 0, 0),  # red
    "MVFR": (0, 0, level * 2),  # blue
    "VFR": (0, level, 0),  # green
}


def extract_tag(metar: str, tag: str, default=""):
    """Extract a tag from a METAR string.

    Args:
        metar: METAR string
        tag: Tag to extract

    Returns:
        Value of tag
    """
    tag_start = metar.find("<" + tag + ">")

    if tag_start == -1:
        print('returning default')
        return default
    
    tag_end = metar.find("</" + tag + ">")
    extract = metar[tag_start + len(tag) + 2 : tag_end]
    if extract == "":
        return default
    return extract

def get_metars(airport_pixel: dict):
    """Call API and update neopixels.

    Args:
        airport_pixel: Dictionary mapping airport ICAO codes to pixel index
    """
    print("get metars")

    API_URL = "https://aviationweather.gov/cgi-bin/data/metar.php?format=xml&ids="    
    API_URL += ",".join(list(airport_pixel))
    print("url = ", API_URL)

    try:
        response = requests.get(API_URL)
    except OSError as e:
        print("problem getting metars")
        print(e)
        return

    metars = response.text.split("<METAR>")

    for metar in metars[1::]:
        flight_category = extract_tag(metar, "flight_category")
        wind_speed_kt = extract_tag(metar, "wind_speed_kt", 0)
        station_id = extract_tag(metar, "station_id")
        pixel = airport_pixel[station_id]
        color = flight_category_rgb[flight_category]
        airport_metar[station_id] = (pixel, color, wind_speed_kt)
        print(f"station_id = {station_id} \t pixel = {pixel} \t flight_category = {flight_category} \t wind_speed_kt = {wind_speed_kt}")

    return


def update_pixels():

    for code in airport_metar:
        pixel = airport_metar[code][0]
        color = airport_metar[code][1]
        gust = airport_metar[code][2]

        if gust:
            freq = 300
            freq = freq - int(gust) * 5

            # pulse between 0.5 and 1.0
            pulse = math.sin(utime.ticks_ms() / freq) + 1
            pulse = 0.5 + (pulse) / 4

            color = [int(rgb * pulse) for rgb in color]
        np[pixel] = color

    np.write()


def flash(i: int):
    """Flash a single pixel to help identify airports.

    Args:
        i: index of neopixel to flash
    """
    np[i] = (25, 25, 25)
    np.write()
    time.sleep(1)
    np[i] = (0, 0, 0)
    np.write()


def test_all():
    """Test all pixels."""
    print("Test pixels")
    for color in [(32, 0, 0), (0, 32, 0), (0, 0, 32), (0, 0, 0)]:
        last = 0
        for pixel in range(lights):
            # np[last] = (0, 0, 0)
            np[pixel] = color
            np.write()
            time.sleep(0.02)  # 0.02)
            last = pixel
        time.sleep(0.2)
        np[last] = (0, 0, 0)


# Split airport_pixel dictionary in 1/2 due to micropython response size handling
# TODO instead of splitting, loop with a modulus of 10 or so
airport_pixel_1 = dict(list(airport_pixel.items())[len(airport_pixel) // 2 :])
airport_pixel_2 = dict(list(airport_pixel.items())[: len(airport_pixel) // 2])


def clear():
    for i in range(lights):
        np[i] = (0, 0, 0)
    np.write()


""" Main loop """
# test the neopixel strip first
# test_all()

while True:
    print("\nloop starts")
    get_metars(airport_pixel_1)

    # 2024-01-13 Testing if these subsequent calls are getting us flagged as abusive
    get_metars(airport_pixel_2)

    update_pixels()
    print("-----\ntime.time() = ", time.time() / 60 / 60, "hr\n")
    start = time.time()

    print('Sleeping 10m')
    while (time.time() - start) < 600:
        update_pixels()
