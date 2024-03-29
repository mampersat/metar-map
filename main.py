""" Neopixel METAR map """

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


def get_metars(airport_pixel: dict):
    """Call API and update neopixels.

    Args:
        airport_pixel: Dictionary mapping airport ICAO codes to pixel index
    """
    print("get metars")

    API_URL = (
        "https://www.aviationweather.gov/adds/dataserver_current/httpparam?"
        "dataSource=metars&requestType=retrieve&format=csv&hoursBeforeNow=5&mostRecentForEachStation=true&"
        "stationString="
    )

    API_URL += ",".join(list(airport_pixel))

    print("url = ", API_URL)

    try:
        response = requests.get(API_URL)
    except:
        print("problem getting metars")
        return
    response_split = response.text.split("\n")
    # If iterating on code that doesn't need live data - maybe not call the API so much
    # test_response = "No errors\nNo warnings\n10 ms\ndata source=metars\n3 results\nraw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m\nKAHN 181741Z 07008KT 1 1/2SM BR OVC005 05/03 A3009 RMK AO2 P0001 T00500028,KAHN,2021-02-18T17:41:00Z,33.95,-83.33,5.0,2.8,70,8,,1.5,30.088583,,,,TRUE,,,,,,BR,OVC,500,,,,,,,IFR,,,,,,0.01,,,,,,SPECI,241.0\nKBOS 181654Z 05006KT 10SM FEW027 BKN033 OVC140 M02/M11 A3044 RMK AO2 SLP308 T10171106,KBOS,2021-02-18T16:54:00Z,42.37,-71.02,-1.7,-10.6,50,6,,10.0,30.43996,1030.8,,,TRUE,,,,,,,FEW,2700,BKN,3300,OVC,14000,,,VFR,,,,,,,,,,,,METAR,4.0\nKBTV 181654Z 00000KT 10SM BKN110 OVC200 M05/M14 A3044 RMK AO2 SLP315 T10501139,KBTV,2021-02-18T16:54:00Z,44.47,-73.15,-5.0,-13.9,0,0,,10.0,30.43996,1031.5,,,TRUE,,,,,,,BKN,11000,OVC,20000,,,,,VFR,,,,,,,,,,,,METAR,101.0\n"
    # response_split = test_response.split("\n")

    # The first 5 lines of the CSV contain headers etc
    for i in range(6, len(response_split)):
        metar = response_split[i].split(",")

        try:
            station_id = metar[1]
            flight_category = metar[30]
            wind_gust_kt = metar[9]
            pixel = airport_pixel[station_id]

            print(station_id, pixel, flight_category, wind_gust_kt)

            color = flight_category_rgb[flight_category]
            airport_metar[station_id] = (pixel, color, wind_gust_kt)
        except:
            print("error parsing metar", metar)


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
test_all()

while True:
    print("\nloop starts")
    get_metars(airport_pixel_1)
    get_metars(airport_pixel_2)
    update_pixels()
    print("-----\ntime.time() = ", time.time() / 60 / 60, "hr\n")
    start = time.time()
    while (time.time() - start) < 600:
        update_pixels()
