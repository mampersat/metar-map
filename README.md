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

## Mac Commands
Terminal connection
```picocom /dev/tty.SLAB_USBtoUART -b 115200```

## Flash pixel for identifying airport -> pixel mapping
>>> def flash(i):
...     np[i] = (255,255,255)
...     np.write()
...     time.sleep(1)
...     np[i] = (0,0,0)
...     np.write()