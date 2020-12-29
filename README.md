# ProtonMagTag
Personal MagTag codebase

Based on code from: https://learn.adafruit.com/magtag-covid-tracking-project-iot-display

Requires CircuitPython 6.x

[wikiquote.py](wikiquote.py) parses Quote of the day from https://en.wikiquote.org/wiki/Main_Page HTML in a single pass, efficiently for microcontroller. I have no benchmarks to prove it is efficient, but XML and regular expression parsing built-ins included in CircuitPy crashed on this dataset when I tried on the MagTag.