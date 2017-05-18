import paho.mqtt.client as mqtt
import json


mqttc = mqtt.Client()
mqttc.connect('127.0.0.1',1883)
app={}


while True:
      app['app_name']=input('enter app name->')
      app['MQTT_TOPIC']=input('mqtt topic->')
      app['MQTT_BROKER']=input('mqtt broker address->')
      app['port']=input('enter port for WSN->')
      ap=json.dumps(app)
      mqttc.publish('fog',ap.encode('utf-8'))
      app={}