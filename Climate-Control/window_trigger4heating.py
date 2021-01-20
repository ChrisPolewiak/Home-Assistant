# Turn Off/On Heating Valve in room on Window/Door Trigger

sensors_db = {
    # sypialnia balkon
    'binary_sensor.0x00158d00024243bc_contact': [ 'climate.sypialnia' ],
    # toaleta okno
    'binary_sensor.0x00158d000275010d_contact': [ 'climate.toaleta', 'climate.toaleta_podloga' ],
    # kuchnia okno
    'binary_sensor.0x00158d00027b25bb_contact': [ 'climate.kuchnia_podloga', 'climate.toaleta_podloga', 'climate.salonpd', 'climate.salonzach' ],
    # salon drzwi taras zach
    'binary_sensor.0x00158d000309ecbe_contact': [ 'climate.kuchnia_podloga', 'climate.toaleta_podloga', 'climate.salonpd', 'climate.salonzach' ],
    # salon drzwi taras pd
    'binary_sensor.0x00158d0001c0a478_contact': [ 'climate.kuchnia_podloga', 'climate.toaleta_podloga', 'climate.salonpd', 'climate.salonzach'  ],
    # salon okno
    'binary_sensor.0x00158d00045b06e5_contact': [ 'climate.kuchnia_podloga', 'climate.toaleta_podloga', 'climate.salonpd', 'climate.salonzach'  ],
    # drzwi wejsciowe
    'binary_sensor.0x00158d00024243a3_contact': [ 'climate.kuchnia_podloga', 'climate.toaleta_podloga', 'climate.salonpd', 'climate.salonzach'  ],
    # maciek balkon
    'binary_sensor.0x00158d0003139ee6_contact': [ 'climate.maciej' ],
    # michal okno
    'binary_sensor.0x00158d000319a65f_contact': [ 'climate.michal' ],
    # garaz drzwiwewn
    'binary_sensor.0x00158d00044f72dd_contact': [ 'climate.toaleta_podloga' ],
    # chris okno
    'binary_sensor.0x00158d00052d5403_contact': [ 'climate.chris' ],
    # jakub okno
    'binary_sensor.0x00158d00053fd96e_contact': [ 'climate.jakub' ],
    # lazienka okno
    'binary_sensor.0x00158d00053fda8f_contact': [ 'climate.lazienka', 'climate.lazienka_podloga' ],
    # poddasze okno
    'binary_sensor.0x00158d00053fdc4e_contact': [],
    # garaz okno
    'binary_sensor.0x00158d00054dad6e_contact': [ 'climate.pralnia_grzejnik', 'climate.garaz_grzejnik' ]
}

locked_to_off = {}
locked_change = {}
locked_default = {}

logger.info( 'Search for open windows:' )
# list all defined contacts sensors
for sensor_id in sensors_db:
    sensor = hass.states.get(sensor_id)

    # list all thermostats matched with sensor
    for thermostat_id in sensors_db[sensor_id]:
        locked_default[ thermostat_id ] = 0

        # if contact is opened
        if sensor.attributes.get('contact') == False:
            logger.debug( ' - opened door/window: ' + sensor.attributes.get('friendly_name') )

            thermostat = hass.states.get( thermostat_id )
            # if thermostat exists (in the event of a possible failure)
            if thermostat:
                locked_change[thermostat_id] = 1

                # is it a thermostat with information about the valve opening level or typical binary switch
                if thermostat.attributes.get('valve_position'):
                    # valve
                    if ( thermostat.state != 'off'):
                        logger.info( ' - opened check: ' + sensor.attributes.get('friendly_name') )
                        logger.info( '   thermostat: ' + thermostat_id + ' --> switch to close' )
                        # switch off thermostat - close
                        hass.services.call('climate', 'turn_off', service_data={'entity_id': thermostat_id})
                else:
                    # switch
                    if ( thermostat.state != 'off'):
                        logger.info( '   thermostat: ' + thermostat_id + ' --> switch to close' )
                        # switch off thermostat - close
                        hass.services.call('climate', 'turn_off', service_data={'entity_id': thermostat_id})

# additional loop to open valves only in room where all windows/doors are closed
# additional validation needed if some contact sensors are matched with the same valves
# for example - sometime one valve control floor heating for more than one room. Opening window in any of this room may close heating
#   and this loop prevent for reopen it even if second room all windows are closed
locked_to_off = {key: locked_change.get(key, locked_default[key]) for key in locked_default} 

logger.info( 'Search for closed windows:' )
# list all defined contacts sensors
for sensor_id in sensors_db:
    sensor = hass.states.get(sensor_id)

    # list all thermostats matched with sensor
    for thermostat_id in sensors_db[sensor_id]:

        # if contact is closed
        if sensor.attributes.get('contact') == True:
            logger.debug( ' - closed door/window: ' + sensor.attributes.get('friendly_name') )

            thermostat = hass.states.get( thermostat_id )

            # if thermostat exists (in the event of a possible failure)
            if thermostat:

                # result of additional loop - if valve was closed in previous step, do not reopen it
                if ( locked_to_off[thermostat_id] == 1 ):
                    logger.info( ' - closed sensor: ' + sensor.attributes.get('friendly_name') )
                    logger.info( '   thermostat: ' + thermostat_id + ' --> leave closed' )
                else:
                    
                    # is it a thermostat with information about the valve opening level or typical binary switch
                    if thermostat.attributes.get('valve_position'):
                        # valve
                        if ( thermostat.state != 'auto'):
                            logger.info( ' - closed sensor: ' + sensor.attributes.get('friendly_name') )
                            logger.info( '   thermostat: ' + thermostat_id + ' --> switch to open' )
                            hass.services.call('climate', 'set_hvac_mode', service_data={'entity_id': thermostat_id, 'hvac_mode': 'auto'})
                    else:
                        # switch
                        if ( thermostat.state != 'heat'):
                            logger.info( ' - closed sensor: ' + sensor.attributes.get('friendly_name') )
                            logger.info( '   switch: ' + thermostat_id + ' --> switch to open' )
                            hass.services.call('climate', 'set_hvac_mode', service_data={'entity_id': thermostat_id, 'hvac_mode': 'heat'})



