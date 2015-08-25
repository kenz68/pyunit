__author__ = 'quocle'
import subprocess
import time

def execute(shell_string):
    print shell_string
    subprocess.call(shell_string, shell=True)
    # wait command execute
    time.sleep(0.1)

def adb_pull():
    execute('rm -f result')
    execute('adb pull /sdcard/result .')

def open_miniterm():
    execute('adb shell "miniterm -s 115200 /dev/ttyHSL1 > /sdcard/result" &')