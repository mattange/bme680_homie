import sys
import time
import logging
import homie
import bme680

from bme680_homie.device_bme680 import Device_BME680


if __name__ == "__main__":

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
        "topic": "homie",
        "fw_name": "homie4",
        "fw_version": homie.__version__,
        "update_interval": 60,
        "implementation": sys.platform,
        }

    dev = Device_BME680(device_id="air-sensor-baby-bedroom",
            name = "Air sensor Baby Bedroom", 
            mqtt_settings=MQTT_SETTINGS,
            homie_settings=HOMIE_SETTINGS)

    logging.info("BME680 starting loop")
    dev.start_publishing_loop()

    try:
        while True:
            # this should be already started and stuff should already be happening
            # as the callbacks are in action... you don't really need the below.
            pass
    except KeyboardInterrupt:
        dev.stop_publishing_loop()
        pass
