__author__ = 'quocle'
result_name = 'result.txt'
a1_preview_sw = 'A1 OPEN'

# open sw
sc_open_sw_a1 = ['00 00 02 00 00 02', 'ccb_cmd_scanning: cmd_received 0000', 'CAM_A1 status has changed to SW STANDBY mode']
sc_open_sw_b1 = ['00 00 40 00 00 02', 'ccb_cmd_scanning: cmd_received 0000', 'CAM_B1 status has changed to SW STANDBY mode']
sc_open_sw_c1 = ['00 00 00 08 00 02', 'ccb_cmd_scanning: cmd_received 0000', 'CAM_C1 status has changed to SW STANDBY mode']
# open hw
sc_open_hw_a1 = ['00 00 02 00 00 01', 'ccb_cmd_scanning: cmd_received 0000', 'CAM_A1 status has changed to HW STANDBY' ]
sc_open_hw_b1 = ['00 00 02 00 00 01', 'ccb_cmd_scanning: cmd_received 0000', 'CAM_A1 status has changed to HW STANDBY' ]
sc_open_hw_c1 = ['00 00 02 00 00 01', 'ccb_cmd_scanning: cmd_received 0000', 'CAM_A1 status has changed to HW STANDBY' ]