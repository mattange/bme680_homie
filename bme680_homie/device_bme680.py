import bme680
from homie.device_base import Device_Base
from homie.node.node_base import Node_Base
from homie.node.property.property_temperature import Property_Temperature
from homie.node.property.property_humidity import Property_Humidity
from homie.node.property.property_pressure import Property_Pressure
from homie.node.property.property_integer import Property_Integer


class Device_BME680(Device_Base):
    def __init__(self, device_id=None, name=None, 
            homie_settings=None, mqtt_settings=None,
            core_update_interval=60):
        super().__init__(device_id, name, homie_settings, mqtt_settings)
        

        # assign sensor
        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except IOError:
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        self._sensor = sensor

        node_upd_interval = Node_Base(self, id="update-interval", name="Core data update interval", type_="status")
        upd_interval = Property_Integer(node=node_upd_interval, 
                                        id="interval", name="Update interval",
                                        unit="s", settable=True, 
                                        set_value=self._set_core_upd_int, 
                                        value=core_update_interval, data_format="5:3600")
        node_upd_interval.add_property(upd_interval)
        self.add_node(node_upd_interval)
        self._upd_interval = upd_interval

        # assign Homie features
        node_barometer = Node_Base(self, id="barometer", name="Pressure sensor", type_="status")
        pressure_prop = Property_Pressure(node=node_barometer, unit="hPa")
        node_barometer.add_property(pressure_prop)
        self.add_node(node_barometer)
        self._pressure = pressure_prop

        node_hygrometer = Node_Base(self, id="hygrometer", name="Humidity sensor", type_="status")
        humidity_prop = Property_Humidity(node=node_hygrometer)
        node_hygrometer.add_property(humidity_prop)
        self.add_node(node_hygrometer)
        self._humidity = humidity_prop

        node_thermometer = Node_Base(self, id="thermometer", name="Temperature sensor", type_="status")
        temperature_prop = Property_Temperature(node=node_thermometer, unit="°C")
        node_thermometer.add_property(temperature_prop)
        self.add_node(node_thermometer)
        self._temperature = temperature_prop

        node_aqi = Node_Base(self, id="aqi",name="Air Quality Index", type_="status")
        aqi_prop = Property_Integer(node=node_aqi, 
                                    id="aqi", name="Air quality",
                                    settable=False)
        node_aqi.add_property(aqi_prop)
        self.add_node(node_aqi)
        self._aqi = aqi_prop

        self.start()   
    
    def get_core_data(self):
        self._sensor.get_sensor_data()
        self._pressure.value = self._sensor.data.pressure
        self._temperature.value = self._sensor.data.temperature
        self._humidity.value = self._sensor.data.humidity

    def _set_core_upd_int(self, value):
        self._upd_interval.value = value

    @property
    def core_update_interval(self):
        return self._upd_interval.value
    @core_update_interval.setter
    def core_update_interval(self, value):
        self._upd_interval.value = value

    #def mqtt_on_message(self, topic, payload, retain == 1, qos):
    #    pass

    
