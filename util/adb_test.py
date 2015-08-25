__author__ = 'quocle'
from util.adb import ADB
debug = ADB()

print debug.devices()

print debug.shell("input keyevent 26")
print debug.shell("input keyevent 82")
print debug.shell("input swipe 50 50 800 50")
print debug.miniterm_open()