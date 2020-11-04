from homie.device_base import Device_Base
from homie.node.node_base import Node_Base
from homie.node.property.property_temperature import Property_Temperature
from homie.node.property.property_humidity import Property_Humidity
from homie.node.property.property_pressure import Property_Pressure
from homie.node.property.property_integer import Property_Integer


class Device_BME680(Device_Base):
    def __init__(self, device_id=None, name=None, 
            homie_settings=None, mqtt_settings=None):
        super().__init__(device_id, name, homie_settings, mqtt_settings)
         
        node_barometer = Node_Base(self, id="barometer", name="Pressure sensor", type_="status")
        pressure_prop = Property_Pressure(node=node_barometer, unit="hPa")
        node_barometer.add_property(pressure_prop)
        self.add_node(node_barometer)
        self.pressure = pressure_prop

        node_hygrometer = Node_Base(self, id="hygrometer", name="Humidity sensor", type_="status")
        humidity_prop = Property_Humidity(node=node_hygrometer)
        node_hygrometer.add_property(humidity_prop)
        self.add_node(node_hygrometer)
        self.humidity = humidity_prop

        node_thermometer = Node_Base(self, id="thermometer", name="Temperature sensor", type_="status")
        temperature_prop = Property_Temperature(node=node_thermometer, unit="°C")
        node_thermometer.add_property(temperature_prop)
        self.add_node(node_thermometer)
        self.temperature = temperature_prop

        node_aqi = Node_Base(self, id="aqi",name="Air Quality Index", type_="status")
        aqi_prop = Property_Integer(node=node_aqi, settable=False)
        node_aqi.add_property(aqi_prop)
        self.add_node(node_aqi)
        self.aqi = aqi_prop

        self.start()   

