#!/usr/bin/python3
import requests
import time
import re
import json
import sys
from datetime import datetime

for line in sys.stdin: 
    if 'q' == line.rstrip(): 
        break

csvdata = line
csvarray = csvdata.split(';')

# Panels ID you have to get from installer or just from DTU
# Using this array you can monitor each Phase
panel_phase = {
	'panel_1-1': 'phase1',
	'panel_1-2': 'phase1',
	'panel_1-3': 'phase1',
	'panel_1-4': 'phase1',
	'panel_2-1': 'phase2',
	'panel_2-2': 'phase2',
	'panel_2-3': 'phase2',
	'panel_2-4': 'phase2',
	'panel_3-1': 'phase3',
	'panel_3-2': 'phase3',
	'panel_3-3': 'phase3',
	'panel_3-4': 'phase3',
}

counter=0
stat_pv_current_power = {}
stat_pv_current_power['phase1'] = 0
stat_pv_current_power['phase2'] = 0
stat_pv_current_power['phase3'] = 0
stat_pv_current_power['total'] = 0
stat_pv_temperature = {}
stat_pv_power = {}

for a in csvarray:
	counter=counter+1
	if (counter == 3):
		stat_energy_today = float(a)
	if (counter == 4):
		stat_co2_saved = float(a)
	if (counter == 8):
		stat_panels_online = int(a)
	if counter>11 and counter<157:
		if (counter-13)%8 == 0:
			panelid = a
			phase = panel_phase[a]
		if (counter-13)%8 == 4:
			panel_current_power = float( re.sub('\s+(\d+)\. (\d+)W', '\\1.\\2', a) )
			stat_pv_power[panelid] = float(panel_current_power)
			stat_pv_current_power[phase] = round( stat_pv_current_power[phase] + panel_current_power , 1)
			stat_pv_current_power['total'] = round( stat_pv_current_power['total'] + panel_current_power, 1)
		if (counter-13)%8 == 6:
			panel_temperature = re.sub('(\d+)\. (\d+)C', '\\1.\\2', a)
			stat_pv_temperature[panelid] = float(panel_temperature)

# Generate stats
data = {}
data['current_power_phase1'] = round(stat_pv_current_power['phase1']/1000,2)
data['current_power_phase2'] = round(stat_pv_current_power['phase2']/1000,2)
data['current_power_phase3'] = round(stat_pv_current_power['phase3']/1000,2)
data['current_power_total'] = round(stat_pv_current_power['total']/1000,2)
data['co2_saved'] = stat_co2_saved
data['energy_today'] = stat_energy_today
data['panels_online'] = stat_panels_online
data['grid_temperature'] = stat_pv_temperature
data['grid_power'] = stat_pv_power

# Prepare valid JSON file for Hassio
jsonStr = json.dumps(data,indent=4)
print( jsonStr )
