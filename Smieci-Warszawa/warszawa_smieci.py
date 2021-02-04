#!/usr/bin/python3
import requests
import time
import re
import json
import sys
import urllib
from urllib.parse import unquote

# Check commandline arguments
# Required one - address
if ( sys.argv[1] ):
    adres = sys.argv[1]
else:
    print ("Podaj adres :'ulica numer, dzielnica'")
    exit()

# Search for addressPointId by Addres
url = 'https://warszawa19115.pl/harmonogramy-wywozu-odpadow?p_p_id=portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=autocompleteResourceURL&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ_name='+adres
r = requests.get(url)
data = r.json()

if ( data ):

    trash_report = {}
    trash_report['adres'] = unquote(data[0]['fullName'])
    addressPointId = data[0]['addressPointId']

    # Get Scheduler by addressPointId
    url = 'https://warszawa19115.pl/harmonogramy-wywozu-odpadow?p_p_id=portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=ajaxResourceURL&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ_addressPointId='+addressPointId
    r = requests.get(url)
    data = r.json()

    # Create report divided by trash fractions
    for harmonogram in data[0]['harmonogramy']:
        if ( harmonogram['frakcja']['id_frakcja'] == 'BK' ):
            trash_report['BIO'] = harmonogram['data']
        if ( harmonogram['frakcja']['id_frakcja'] == 'MT' ):
            trash_report['TWORZYWA'] = harmonogram['data']
        if ( harmonogram['frakcja']['id_frakcja'] == 'OP' ):
            trash_report['PAPIER'] = harmonogram['data']
        if ( harmonogram['frakcja']['id_frakcja'] == 'OS' ):
            trash_report['SZKLO'] = harmonogram['data']
        if ( harmonogram['frakcja']['id_frakcja'] == 'OZ' ):
            trash_report['ZIELONE'] = harmonogram['data']
        if ( harmonogram['frakcja']['id_frakcja'] == 'WG' ):
            trash_report['WIELKOGABARYTOWE'] = harmonogram['data']
        if ( harmonogram['frakcja']['id_frakcja'] == 'ZM' ):
            trash_report['ZMIESZANE'] = harmonogram['data']

    # Export JSON
    jsonStr = json.dumps(trash_report,indent=4)
    print ( jsonStr )



