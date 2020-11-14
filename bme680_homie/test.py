import sys
import time
import homie
import bme680

from device_bme680 import Device_BME680

MQTT_SETTINGS = {
    'MQTT_BROKER': 'mqtt.lan.rocketmacro.com',
    'MQTT_PORT': 8883,
    'MQTT_USERNAME': 'sensor',
    'MQTT_PASSWORD': 'sensor_pwd',
    'MQTT_CLIENT_ID': 'air-sensor-baby-bedroom',
    'MQTT_KEEPALIVE': 60,
    'MQTT_USE_TLS': True

}

HOMIE_SETTINGS = {
    "version": "4.0.0",
    "topic": "home/sensors",
    "fw_name": "homie4",
    "fw_version": homie.__version__,
    "update_interval": 60,
    "implementation": sys.platform,
}

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

dev = Device_BME680(device_id="air-sensor-baby-bedroom",
        name = "Air sensor Baby Bedroom", 
        mqtt_settings=MQTT_SETTINGS,
        homie_settings=HOMIE_SETTINGS)

try:
    while True:
        dev.get_core_data()
        print('should have published data')
#        if sensor.get_sensor_data():
#            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
#                sensor.data.temperature,
#                sensor.data.pressure,
#                sensor.data.humidity)
#            
#            dev.temperature.value = sensor.data.temperature
#            dev.pressure.value = sensor.data.pressure
#            dev.humidity.value = sensor.data.humidity
#
#            if sensor.data.heat_stable:
#                print('{0},{1} Ohms'.format(
#                    output,
#                    sensor.data.gas_resistance))
#
#            else:
#                print(output)

        time.sleep(dev.core_update_interval)

except KeyboardInterrupt:
    pass
