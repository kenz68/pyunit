import argparse
import string
import subprocess
import sys
import re
from random import randint

atypecam = [ 'a1', 'a2', 'a3', 'a4', 'a5' ]
path = '/sys/class/light_ccb/i2c_interface/i2c_w'
asic_path = '/sys/devices/soc.0/f9923000.spi/spi_master/spi0/spi0.0/'
asic_path_read = asic_path + 'read'
asic_path_write = asic_path + 'write'
max_range = 65535
_2bytes = '0x00 0x00'

def execute(cmd):
    print(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return proc.communicate()[0]
    pass

def split_bytes(arg):
    fstring = arg[0:4] + ' 0x' + arg[-2:]
    return fstring

def convert_to_hex(arg):
    fstring = arg
    rs = 0
    int_rs = 0;
    if arg.find("0x") != -1:
        rs = arg
    else:
        int_rs =  int(arg)
        rs = hex(int_rs)

    if (int_rs <= 0xf): # one nibble
        fstring = '0x00 0x0' + rs[-1:]
    elif (int_rs <= 255): # two nibbles
        fstring = '0x00 ' + rs
    elif (int_rs <= 4095): # three nibbles
        fstring = '0x0' + rs[-3:-2] + ' 0x' + rs[-2:]
    else: # four nibbles
        fstring = '0x' + rs[-4:-2] + ' 0x' + rs[-2:]
    return fstring
# my func
def remove_duplicate(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
def add_hex(a, b):
    return  hex(int(eval(a)) + int(eval(b)))
def add_bitmask(a, b):
    lsta = a.split(' ')
    lstb = b.split(' ')
    lstc = []
    for i in range(0, len(lsta)):
        lstc.append(add_hex(lsta[i], lstb[i]))
    for i in range(0,len(lstc)):
        lstc[i] = format(int(lstc[i], 16), '#04x')
    # return lstc
    bitmask = " ".join(lstc)
    return bitmask

def get_stream_data(data):
    stream_data = '0x'
    datas = data.split(':')
    # CSI
    if len(datas) == 2:
        if datas[0] == 'cs0':
            stream_data += '1'
        elif datas[0] == 'cs1':
            stream_data += '2'
        elif datas[0] == 'cs01':
            stream_data += '3'
    # Stream mode
        if datas[1] == 'on':
            stream_data += '1'
        elif datas[1] == 'off':
            stream_data += '0'
    if len(stream_data) != 4:
        parser.print_help()
        sys.exit()
    return ' ' + stream_data + ' ' + _2bytes


def get_m_bitmask(list_cams):
    m_bitmask = "0x00 0x00 0x00"
    for i in range(0, len(list_cams)):
        # print(module_bitmask(list_cams[i]))
        m_bitmask = add_bitmask(m_bitmask, module_bitmask(list_cams[i]))
    return m_bitmask

def module_bitmask(x):
    return {
        'g' : "0x01 0x00 0x00",
        'a1': "0x02 0x00 0x00",
        'a2': "0x04 0x00 0x00",
        'a3': "0x08 0x00 0x00",
        'a4': "0x10 0x00 0x00",
        'a5': "0x20 0x00 0x00",
        'b1': "0x40 0x00 0x00",
        'b2': "0x80 0x00 0x00",
        'b3': "0x00 0x01 0x00",
        'b4': "0x00 0x02 0x00",
        'b5': "0x00 0x04 0x00",
        'c1': "0x00 0x08 0x00",
        'c2': "0x00 0x10 0x00",
        'c3': "0x00 0x20 0x00",
        'c4': "0x00 0x40 0x00",
        'c5': "0x00 0x80 0x00",
        'c6': "0x00 0x00 0x01",
    }[x]

def module_ucid(x):
    return {
        'disable' : "0x00 0x00", # b'0000: Disabled
        'unused'  : "0x00 0x01",
        'debug'   : "0x00 0x02", # b'0010: Debug
        'preview' : "0x00 0x03", # b'0011: Preview
        'hires'   : "0x00 0x05", # b'0101: Hi-res still capture
        'focal'   : "0x00 0x06", # b'0110: Focal Stacking capture
        'hdr'     : "0x00 0x07", # b'0111: HDR still capture
        'video'   : "0x00 0x04", # b'0100: Video
        'ftmq'    : "0x00 0x09", # b'1001: Factory Test Mode (FTM): Quick Check
        'ftmc'    : "0x00 0x0a", # b'1010: Factory Test Mode (FTM): Calibration
    }[x]

def module_command(x):
    random_ucid = format(randint(0, max_range), '#06x')
    return {
        'ucid'          : random_ucid + " 0x10 0x00",
        'open'          : random_ucid + " 0x00 0x00",
        'stream'        : random_ucid + " 0x00 0x02",
        'focus'         : random_ucid + " 0x00 0x48",
        'mirror'        : random_ucid + " 0x00 0x44",
        'exposure'      : random_ucid + " 0x00 0x32",
        'resolution'    : random_ucid + " 0x00 0x2C",
        'gain'          : random_ucid + " 0x00 0x30",
        'fps'           : random_ucid + " 0x00 0x50",
        'vcmpos'        : random_ucid + " 0x00 0x3C",
        'temperature'   : random_ucid + " 0x02 0x1C",
        'status'        : "0x0000 0x00 0x28",
    }[x]

parser = argparse.ArgumentParser()
parser.add_argument("-h, --help", help="show help",
                    action="store")
parser.add_argument("-v, --verbose", help="increase output verbosity",
                    action="store")
parser.add_argument("-c", "--camera", help="select camera: from a1->a5, b1->b5 or c1->c6",
                    action="store")
parser.add_argument("-f", "--focus", help="select focus distance",
                    action="store")
parser.add_argument("-m", "--mirror", help="select mirror angle",
                    action="store")
parser.add_argument("-e", "--exposure", help="select exposure value",
                    action="store")
parser.add_argument("-r", "--resolution", help="select resolution value ([X resolution]:[Y resolution])",
                    action="store")
parser.add_argument("-s", "--stream", help="stream [csi]:[on/off] a camera",
                    action="store")
parser.add_argument("-g", "--gain", help="select gain|sensitivity value",
                    action="store")
parser.add_argument("-o", "--open", help="camera open hw/sw/close a camera",
                    action="store")
parser.add_argument("-p", "--fps", help="select frames per second",
                    action="store")
parser.add_argument("-t", "--test", help="manual type command",
                    action="store")
parser.add_argument("-mode", "--mode", help="set mode demo/new",
                    action="store")
parser.add_argument("-u", "--ucid", help="set Active Use Case ID. ",
                    action="store")
parser.add_argument("-vp", "--vcmpos", help="set Cam Module VCM Position. ",
                    action="store")
parser.add_argument("-ms", "--status", help="get Module Status. use -> [-ms get]",
                    action="store")
parser.add_argument("-tmp", "--temperature", help="Get temperature value [-tmp get]",
                    action="store")
args = parser.parse_args()

if args.test:
    execute(args.test)
    sys.exit()
if args.ucid:
    if not args.camera:
        ucid_string = "adb shell \"echo 4 "+ module_command('ucid') + " " + module_ucid(args.ucid) + " > " + path + "\""
        execute(ucid_string)
        sys.exit()
if args.temperature:
    temperature_string = "adb shell \"echo 2 " + module_command('temperature') + " > "+ path + "\""
    execute(temperature_string)
    sys.exit()
if args.camera:
    cams = args.camera.split(',')
    if len(cams) == 1:
        m_bitmask = module_bitmask(args.camera)
    else:
        cams = remove_duplicate(cams)
        m_bitmask = get_m_bitmask(cams)
else:
    parser.print_help()
    sys.exit()

if args.open:
    if args.camera == "g":
        if args.open == "hw":
            open_string = "adb shell \"echo 6 " + module_command('open') + " " + m_bitmask + " 0x01 > "+ path + "\""
            execute(open_string)
        elif args.open == "sw":
            open_string = "adb shell \"echo 6 " + module_command('open') + " " + m_bitmask + " 0x02 > "+ path + "\""
            execute(open_string)
        elif args.open == "close":
            open_string = "adb shell \"echo 6 " + module_command('open') + " " + m_bitmask + " 0x00 > "+ path + "\""
            execute(open_string)
        else:
            parser.print_help()
            sys.exit()
    else:
        fstring = ""
        list_open = args.open.split(",")
        if len(cams) == len(list_open):
            for i in range(0, len(cams)):
                if list_open[i] == "hw":
                    fstring += "0x01 "
                elif list_open[i] == "sw":
                    fstring +=  "0x02 "
                elif list_open[i] == "close":
                    fstring += "0x00 "
                else:
                    parser.print_help()
                    sys.exit()
        ucid = 2 + 3 + len(cams)
        open_string = "adb shell \"echo "+ str(ucid) +" " + module_command('open') + " " + m_bitmask + " " + fstring + "> "+ path + "\""
        execute(open_string)

if args.stream:
    if args.camera == "g":
        stream_string = "adb shell \"echo 8 " + module_command('stream') + " " + m_bitmask + get_stream_data(args.stream) +" > "+ path + "\""
        execute(stream_string)
    else:
        fstring = ""
        list_stream = args.stream.split(",")
        if len(cams) == len(list_stream):
            for i in range(0, len(cams)):
                fstring += get_stream_data(list_stream[i])
        ucid = 2 + 3 + 3*len(cams)
        stream_string = "adb shell \"echo "+ str(ucid) +" " + module_command('stream') + " " + m_bitmask + fstring + " > "+ path + "\""
        execute(stream_string)
if args.mirror:
    fstring = convert_to_hex(args.mirror)
    #fstring = args.mirror
    print "Mirror is " + args.mirror
    if (args.camera in atypecam):
        # 35mm
        print "no mirrors for 35mm, exiting"
        sys.exit()
    else:
        # 70mm
        mirror_string = "adb shell \"echo 7 " + module_command('mirror') + " " + m_bitmask + " " + fstring + " > "+ path + "\""
    execute(mirror_string)
    print ""

if args.exposure:
    if args.ucid:
        m_bitmask  += " " + module_ucid(args.ucid)
    else:
        print "Please set UCID"
        sys.exit()
    if args.camera == "g":
        if args.mode == 'demo':
            fstring = convert_to_hex(args.exposure) + ' ' + _2bytes + ' ' + _2bytes + ' ' + _2bytes
        else:
            fstring = _2bytes + ' ' + _2bytes + ' ' + _2bytes + ' '+ convert_to_hex(args.exposure)
        exposure_string = "adb shell \"echo 15 " + module_command('exposure') + " " + m_bitmask + " " + fstring + " > "+ path + "\""
    else:
        fstring = ""
        list_exposure = args.exposure.split(",")
        if len(cams) == len(list_exposure):
            for i in range(0, len(cams)):
                if args.mode == 'demo':
                    fstring += convert_to_hex(list_exposure[i]) + ' ' + _2bytes + ' ' + _2bytes + ' ' + _2bytes + ' '
                else:
                    fstring += _2bytes + ' ' + _2bytes + ' ' + _2bytes + ' '+ convert_to_hex(list_exposure[i]) + " "
        ucid = 2 + 3 + 2 + 8*len(cams)
        exposure_string = "adb shell \"echo "+ str(ucid) +" " + module_command('exposure') + " " + m_bitmask + " " + fstring + "> "+ path + "\""
    execute(exposure_string)
    print ""

if args.resolution:
    if args.ucid:
        m_bitmask  += " " + module_ucid(args.ucid)
    else:
        print "Please set UCID"
        sys.exit()
    if args.camera == "g":
        fstring = args.resolution
        res = fstring.split(':')
        resX = _2bytes + ' ' + convert_to_hex(res[0])
        resY = _2bytes + ' ' + convert_to_hex(res[1])
        fstring = resX + " " + resY
        resolution_string = "adb shell \"echo 15 " + module_command('resolution') + " " + m_bitmask + " " + fstring + " > "+ path + "\""
    else:
        fstring = ""
        list_gain = args.resolution.split(",")
        if len(cams) == len(list_gain):
            for i in range(0, len(cams)):
                res = list_gain[i].split(':')
                resX = _2bytes + ' ' + convert_to_hex(res[0])
                resY = _2bytes + ' ' + convert_to_hex(res[1])
                fstring += resX + " " + resY + " "
        else:
            parser.print_help()
            sys.exit()

        ucid = 2 + 3 + 2 + 8*len(cams)
        resolution_string = "adb shell \"echo "+ str(ucid) +" " + module_command('resolution') + " " + m_bitmask + " " + fstring + "> "+ path + "\""
    execute(resolution_string)
    print ""

if args.gain:
    if args.ucid:
        m_bitmask  += " " + module_ucid(args.ucid)
    else:
        print "Please set UCID"
        sys.exit()
    if args.camera == "g":
        fstring = convert_to_hex(args.gain)
        if args.mode == 'demo':
            fstring = fstring + ' ' + _2bytes
        else:
            fstring = _2bytes + ' ' +fstring
        gain_string = "adb shell \"echo 11 " + module_command('gain') + " " + m_bitmask + " " + fstring + " > "+ path + "\""
    else:
        fstring = ""
        list_gain = args.gain.split(",")
        if len(cams) == len(list_gain):
            for i in range(0, len(cams)):
                if args.mode == 'demo':
                    fstring += convert_to_hex(list_gain[i]) + ' ' + _2bytes + ' '
                else:
                    fstring += _2bytes + ' ' + convert_to_hex(list_gain[i]) + " "
        else:
            parser.print_help()
            sys.exit()

        ucid = 2 + 3 + 2 + 4*len(cams)
        gain_string = "adb shell \"echo "+ str(ucid) +" " + module_command('gain') + " " + m_bitmask + " " + fstring + "> "+ path + "\""
    execute(gain_string)
    print ""

if args.fps:
    if args.ucid:
        m_bitmask  += " " + module_ucid(args.ucid)
    else:
        print "Please set UCID"
        sys.exit()
    if args.camera == "g":
        fstring = convert_to_hex(args.fps)
        fps_string = "adb shell \"echo 9 " + module_command('fps') + " " + m_bitmask + " " + fstring + " > "+ path + "\""
    else:
        fstring = ""
        list_fps = args.fps.split(",")
        if len(cams) == len(list_fps):
            for i in range(0, len(cams)):
                fstring += convert_to_hex(list_fps[i]) + ' '
        else:
            parser.print_help()
            sys.exit()

        ucid = 2 + 3 + 2 + 2*len(cams)
        fps_string = "adb shell \"echo "+ str(ucid) +" " + module_command('fps') + " " + m_bitmask + " " + fstring + "> "+ path + "\""
    execute(fps_string)
if args.vcmpos:
    if args.ucid:
        m_bitmask  += " " + module_ucid(args.ucid)
    else:
        print "Please set UCID"
        sys.exit()
    if args.camera == "g":
        fstring = convert_to_hex(args.vcmpos)
        vcmpos_string = "adb shell \"echo 9 " + module_command('vcmpos') + " " + m_bitmask + " " + fstring + " > "+ path + "\""
    else:
        fstring = ""
        list_vcmpos = args.vcmpos.split(",")
        if len(cams) == len(list_vcmpos):
            for i in range(0, len(cams)):
                fstring += convert_to_hex(list_vcmpos[i]) + " "
        else:
            parser.print_help()
            sys.exit()

        ucid = 2 + 3 + 2 + 2*len(cams)
        vcmpos_string = "adb shell \"echo " + str(ucid) +" " + module_command('vcmpos') + " " + m_bitmask + " " + fstring + "> "+ path + "\""
    execute(vcmpos_string)
if args.focus:
    if args.ucid:
        m_bitmask  += " " + module_ucid(args.ucid)
    else:
        print "Please set UCID"
        sys.exit()
    if args.camera == "g":
        fstring = convert_to_hex(args.focus)
        focus_string = "adb shell \"echo 11 " + module_command('focus') + " " + m_bitmask + ' ' + _2bytes + ' ' + fstring + " > "+ path + "\""
    else:
        fstring = ""
        list_focus = args.focus.split(",")
        if len(cams) == len(list_focus):
            for i in range(0, len(cams)):
                fstring += _2bytes + ' ' + convert_to_hex(list_focus[i]) + " "
        else:
            parser.print_help()
            sys.exit()

        ucid = 2 + 3 + 2 + 4*len(cams)
        focus_string = "adb shell \"echo "+ str(ucid) +" " + module_command('focus') + " " + m_bitmask + " " + fstring + "> "+ path + "\""
    execute(focus_string)
if args.status:
    status_string = "adb shell \"echo 5 " + module_command('status') + " " + m_bitmask + " > "+ path + "\""
    execute(status_string)