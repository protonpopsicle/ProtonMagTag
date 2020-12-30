import time
import terminalio
from adafruit_magtag.magtag import MagTag
from wikiquote import get_qotd


# Change this to the hour you want to check the data at
DAILY_UPDATE_HOUR = 5

magtag = MagTag()

# main text, index 0
magtag.add_text(
#    text_font="Arial-12.bdf",
    text_font=terminalioFONT,
    text_position=(8, 8),
    line_spacing=1.0,
    text_wrap=45,
    text_anchor_point=(0, 0),
)

magtag.peripherals.neopixels.brightness = 0.1
magtag.peripherals.neopixel_disable = False # turn on lights
magtag.peripherals.neopixels.fill(0x0F0000) # red

try:
    magtag.get_local_time()
except Exception as e:
    print(e)
    minutes = 60 * 6
    print("Gonna zzz for %d minutes" % minutes)
    magtag.exit_and_deep_sleep(60 * minutes)

try:
    now = time.localtime()
    print("Now:", now)

    # display the current time since its the last-update
    updated_at = "%d/%d\n%d:%02d" % now[1:5]

    # efficiently scrape quote from Wikiquote Main Page
    text = get_qotd(magtag.network.requests)
    print("==>", text)
    magtag.set_text(text, 0)

    # OK we're done!
    magtag.peripherals.neopixels.fill(0x000F00) # green
except (ValueError, RuntimeError) as e:
    print("Some error occured, trying again later -", e)

time.sleep(2) # let screen finish updating

# we only wanna wake up once a day, around the event update time:
event_time = time.struct_time((now[0], now[1], now[2],
                               DAILY_UPDATE_HOUR, 0, 0,
                               -1, -1, now[8]))
# how long is that from now?
remaining = time.mktime(event_time) - time.mktime(now)
if remaining < 0:             # ah its aready happened today...
    remaining += 24 * 60 * 60 # wrap around to the next day
remaining_hrs = remaining // 3660
remaining_min = (remaining % 3600) // 60
print("Gonna zzz for %d hours, %d minutes" % (remaining_hrs, remaining_min))

# Turn it all off and go to bed till the next update time
magtag.exit_and_deep_sleep(remaining)
