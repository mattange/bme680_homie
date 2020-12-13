import bme680
from homie.device_base import Device_Base
from homie.node.node_base import Node_Base
from homie.node.property.property_temperature import Property_Temperature
from homie.node.property.property_humidity import Property_Humidity
from homie.node.property.property_pressure import Property_Pressure
from homie.node.property.property_integer import Property_Integer
from homie.node.property.property_float import Property_Float
from homie.support.repeating_timer import Repeating_Timer


class Device_BME680(Device_Base):
    
    _MAX_RESISTANCE = 250000
    _MIN_RESISTANCE = 50000
    _HUMIDITY_WEIGHT = 0.25
    _upd_interval = 60
    _ideal_rel_humidity = 40


    def __init__(self, device_id=None, name=None, 
            homie_settings=None, mqtt_settings=None):
        super().__init__(device_id, name, homie_settings, mqtt_settings)
        
        # assign sensor
        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except IOError:
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        #sensor.set_humidity_oversample(bme680.OS_2X)
        #sensor.set_pressure_oversample(bme680.OS_4X)
        #sensor.set_temperature_oversample(bme680.OS_8X)
        #sensor.set_filter(bme680.FILTER_SIZE_3)
        #sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        sensor.set_gas_heater_temperature(320)
        sensor.set_gas_heater_duration(150)
        sensor.select_gas_heater_profile(0)
        self._sensor = sensor


        # assign Homie features to update/request information on demand
        node_worker = Node_Base(self, id="worker-node", name="Data worker node", type_="status")
        self.add_node(node_worker)
 
        upd_interval = Property_Integer(node=node_worker, 
                id="update-interval", name="Statistics update interval", 
                unit="s", settable=True, set_value=self._set_upd_interval, 
                value=self._upd_interval, data_format="5:3600")
        node_worker.add_property(upd_interval)
   
        ideal_rel_humidity = Property_Integer(node=node_worker,
                id="update-ideal-rel-humidity", name="Update ideal relative humidity for AQI calculations",
                unit="%", settable=True, set_value=self._set_ideal_rel_humidity,
                value=self._ideal_rel_humidity, data_format="0:100")
        node_worker.add_property(ideal_rel_humidity)

        # assign Homie features to base sensor
        node_sensor = Node_Base(self, id="multi-sensor", name="Multiple sensor", type_="status")
        self.add_node(node_sensor)

        pressure_prop = Property_Pressure(node=node_sensor, unit="hPa")
        node_sensor.add_property(pressure_prop)
        self._pressure = pressure_prop
        humidity_prop = Property_Humidity(node=node_sensor)
        node_sensor.add_property(humidity_prop)
        self._humidity = humidity_prop
        temperature_prop = Property_Temperature(node=node_sensor, unit="°C")
        node_sensor.add_property(temperature_prop)
        self._temperature = temperature_prop
        gas_res_prop = Property_Float(node=node_sensor, id="gas-resistance", name="Gas resistance", settable=False, unit="Ohm")
        node_sensor.add_property(gas_res_prop)
        self._gas_resistance = gas_res_prop
        aqi_prop = Property_Integer(node=node_sensor, id="aqi", name="Air quality index", settable=False)
        node_sensor.add_property(aqi_prop)
        self._aqi = aqi_prop


        # start 
        self.start()
    
    def _get_core_data(self):
        if self._mqtt_connected:
            self._sensor.get_sensor_data()
            self._pressure.value = self._sensor.data.pressure
            self._temperature.value = self._sensor.data.temperature
            self._humidity.value = self._sensor.data.humidity
            if self._sensor.data.heat_stable:
                self._gas_resistance.value = self._sensor.data.gas_resistance
        else:
            pass

    def _publish_data(self):
        if self.mqtt_client.mqtt_connected:
            self._get_core_data()

    @property
    def ideal_rel_humidity(self):
        return self._ideal_rel_humidity
    #needed for set_value routine in node Property
    def _set_ideal_rel_humidity(self):
        self.ideal_rel_humidity = value
    @ideal_rel_humidity.setter
    def ideal_rel_humidity(self,value):
        self._ideal_rel_humidity = value

    @property
    def upd_interval(self):
        return self._upd_interval
    #needed for set_value routine in node Property
    def _set_upd_interval(self, value):
        self.upd_interval = value
    @upd_interval.setter
    def upd_interval(self, value):
        self._upd_interval = value
        self._timer_upd_interval.interval = value

    def start_publishing_loop(self):
        # assign timer to publish info
        self._timer_upd_interval = Repeating_Timer(self._upd_interval)
        self._timer_upd_interval.add_callback(self._publish_data)

    def stop_publishing_loop(self):
        try:
            if self._timer_upd_interval.timer.is_alive():
                self._timer_upd_interval.stop()
        except AttributeError:
            pass
