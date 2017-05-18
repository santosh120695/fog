import subprocess
import threading
import paho.mqtt.client as mqtt
import json
import os


global mqttc,serv_topic,fog_topic
serv_topic='server' #server topic to communicate with server
fog_topic='fog'  # fog topic to communicate with fog 


def on_connect(mosq, obj, rc):
    global mqttc
    mqttc.subscribe((fog_topic,0)) #subscribe to fog topic



def on_message(mosq, obj, msg):
    msg=msg.payload.decode('utf-8')
    msg=json.loads(msg)
    print(msg)
    f=open('config/'+msg['app_name']+'.txt','w') #saves configuration in conf folder
    f.write(json.dumps(msg))
    f.close()
    subprocess.Popen(['python','main.py',msg['app_name']]) # starts application


# for sending messages to server
# not completed
def pub(msg):
    global mqttc,serv_topic
    mqttc.publish(serv_topic,msg.encode('utf-8'))




if __name__=='__main__':
    mqttc = mqtt.Client() # Mqtt object
    mqttc.on_connect = on_connect
    mqttc.on_message=on_message
    mqttc.connect('127.0.0.1',1883) #connecting to mqtt
    subprocess.Popen(['python','linker.py']) #starting linker to allow processes to stream data
    f=os.listdir('config') #no of app present in config file
    df={} 
    # starts all apps 
    for i in f:
        print(i)
        f=open('config/'+i,'r')
        df=json.loads(f.read())
        print(df)
        subprocess.Popen(['python','main.py',df['app_name']]) #starts apps

    mqttc.loop_forever()
