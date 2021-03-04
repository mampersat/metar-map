# neopixels
Time for this neopixel based stuff to all live here

[Flash instructions](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html)

## Things to install
* picocom

```
sudo apt-get install picocom
```

* ampy

```
sudo apt-get install python3-pip
pip3 install adafruit-ampy
```

## WEBRepl Connection

[http://micropython.org/webrepl/#192.168.1.103:8266/](http://micropython.org/webrepl/#192.168.1.103:8266/)

## Commands
Terminal connection MAC
```
picocom /dev/tty.SLAB_USBtoUART -b 115200
```

Terminal connection linux
```
picocom /dev/ttyUSB0 -b 115200
```

Transfer main.py to board
```
ampy -p /dev/ttyUSB0 put main.py
```

## URL to test API stuff
https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=5&mostRecentForEachStation=true&stationString=KBTV

Map: https://www.aviationweather.gov/metar

