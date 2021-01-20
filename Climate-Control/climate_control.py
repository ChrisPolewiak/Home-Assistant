
# All thermostats (binary switch)
thermostats_switch_db = {
    'climate.kuchnia_podloga',
    'climate.lazienka_podloga',
    'climate.toaleta_podloga',
    'climate.chris',
    'climate.sypialnia',
    'climate.salonpd',
    'climate.salonzach',
    'climate.jakub',
    'climate.maciej',
    'climate.michal',
    'climate.toaleta',
    'climate.lazienka',
}
# All thermostats (analog valves)
thermostats_analog_db = {
#    'climate.pralnia_grzejnik',
#    'climate.garaz_grzejnik',
}
# Minimum value of valve opened count as thermostat opened
min_valve_position_required = 30

# Minimum amount of thermostats opened trigger furnace switch on
min_thermostats_opened_required = 1

# Entity ID for Furnace control
furnace_id = 'switch.mqtt_heating_furnace'

count_thermostats_opened=0

# Check status for each thermostats with binary switch
for thermostat_id in thermostats_switch_db:
    thermostat = hass.states.get(thermostat_id)

    # if thermostat exists
    if thermostat:

        # get current thermostat state
        hvac_action = thermostat.attributes.get('hvac_action')
        logger.info( '- ' + thermostat.attributes.get('friendly_name') + ' = ' + hvac_action)

        # if heating - add to number of opened thermostats
        if hvac_action == 'heating':
            count_thermostats_opened = count_thermostats_opened + 1


# Check status for each thermostats with analog valve
for thermostat_id in thermostats_analog_db:
    thermostat = hass.states.get(thermostat_id)

    # if thermostat exists
    if thermostat:
        valve_position = thermostat.attributes.get('valve_position')
        logger.info( '- ' + thermostat.attributes.get('friendly_name') + ' = ' + str(valve_position) + '%')
        if valve_position >= min_valve_position_required:
            count_thermostats_opened = count_thermostats_opened + 1


logger.info('count_thermostats_opened for ' +str(count_thermostats_opened) + ' valves')

# Get current state of furnace
heating_furnace = hass.states.get( furnace_id )
logger.info('current heating state = ' + heating_furnace.state)

# If heating needed and furnace is switched off - turn on furnace
if ( count_thermostats_opened >= min_thermostats_opened_required and heating_furnace.state=='off' ):
    logger.info('Switch on heating')
    hass.services.call('switch', 'turn_on', service_data={'entity_id': furnace_id})

# If heating is not needed and furnace is switched on - turn off furnace
elif ( count_thermostats_opened < min_thermostats_opened_required and heating_furnace.state=='on' ):
    logger.info('Switch off heating')
    hass.services.call('switch', 'turn_off', service_data={'entity_id': furnace_id})
