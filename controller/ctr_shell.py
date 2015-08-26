__author__ = 'quocle'
import subprocess
import time

def execute(shell_string):
    print shell_string
    subprocess.call(shell_string, shell=True)
    # wait command execute
    time.sleep(1)

def adb_pull():
    execute('rm -f result')
    execute('adb pull /sdcard/result .  ')

def open_miniterm():
    execute('adb shell "miniterm -s 115200 /dev/ttyHSL1 > /sdcard/result" &')

def get_log(fname):
    f = open(fname, 'r')
    lines = f.readlines()
    info = []
    for line in lines:
        if 'INFO' in line:
            print line
            info.append(line)
    print info
    f.close()
    return info
