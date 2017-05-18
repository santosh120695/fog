""""
Program for managing wireless sensor network

first data send by client
if pub >
type:""

if sub?
type:topic

next 

sends just data

"""

import asyncio
import threading
import time
import pipes
import sys
import socket


global app_name,loop,soc,client_list,pipe_pub_topic,pipe_sub_topic

@asyncio.coroutine
def server_init(address):
    #server init
    global soc ,loop
    soc=socket.socket()
    soc.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    soc.bind((address))
    soc.listen(30)
    soc.setblocking(False)
    #---------------------------
    # connection acceptance 
    while True:
          c,a=yield from loop.sock_accept(soc) #accepts connection request from client
          msg=yield from loop.sock_recv(c,32) # accepts message from client
          msg=msg.decode('utf-8').split(':') 
          if msg[0]=='pub':  #checks for publisher or subscriber
             loop.create_task(read_client(c)) # starts task to read client 
          elif msg[0]=='sub':
               if msg[1] not in client_list: 
                  client_list[msg[1]]=[]  
                  threading.Thread(target=write_clients,args=(msg[1])).start() # starts task to listen for the topic
               client_list[msg[1]].append(c) # adds client to the list of clients with same topic

@asyncio.coroutine
def read_client(client):
    p=pipes.pipes('pub',pipe_pub_topic) # connects with linker as pulisher
    while True:
          data=yield from loop.sock_recv(client,32) # recv data  from sensor
          print(data)
          data=data.decode('utf-8')
          if data=="": # checks for discoonection
             print('break')
             break
          p.write_pipes(data) # sends data to linker 
              


def write_client(topic):
    pipe_sub_topic=app_name+'_'+topic 
    p=pipes.pipes('sub',pipe_sub_topic) # connects with linker as subscriber
    while True:
          data=p.read_pipes()   # check for data send by linker
          for c in client_list[topic]: # loops through client under same topic
              try:
                  loop.sock_sendall(c,data) # sends data to client

              except:
                     pass



if __name__=='__main__':
    global app_name,loop,pipe_pub_topic,pipe_sub_topic
    port=int(sys.argv[1]) #recv port no
    app_name=sys.argv[2] # app name 
    pipe_pub_topic=app_name+'_wsn' # topic under which sensor data needed to send to linker
    loop=asyncio.get_event_loop()
    loop.create_task(server_init(('0.0.0.0',port)))
    loop.run_forever()
