import paho.mqtt.client as mqtt
import threading,pipes,sys
import json
global buff
import time
buff=[]



def pipe_readder(topic,topic_serv):
    global buff
    pipe=pipes.pipes('sub',topic)
    while True:
          msg=pipe.read_pipes()
          print(msg)
          mqttc.publish(topic_serv,msg)
          buff.append(msg)


def pubb(topic_serv):
    global buff
    t=time.time()
    while True:
         if len(buff)!=0:
            msg=buff.pop(0)
            print(time.time()-t)
            t=time.time()
            mqttc.publish(topic_serv,msg)





if __name__=='__main__':
    mqttc=mqtt.Client()
    app=sys.argv[1]
    f=open('config/'+str(app)+'.txt','r')#reads configuration 
    app_config=f.read()
    f.close()
    app_config=json.loads(app_config) 
    topic_read_pipe=app_config['app_name']+'_wsn'
    MQTT_BROKER=app_config['MQTT_BROKER']
    MQTT_TOPIC=app_config['MQTT_TOPIC']
    mqttc.connect(MQTT_BROKER,1883)
    threading.Thread(target=pipe_readder,args=(topic_read_pipe,MQTT_TOPIC,)).start()#recv data from linker
    threading.Thread(target=pubb,args=(MQTT_TOPIC,)).start() #starts publisher
