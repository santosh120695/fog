import socket
import time
import threading

def fd():
    soc=socket.socket()
    soc.connect(('127.0.0.1',9009))
    msg='pub//iot'
    soc.send(msg.encode('utf-8'))
    i=0
    time.sleep(1)
    while True:
          i+=1
          soc.send(str(i).encode('utf-8'))
          time.sleep(2)


n=10
for j in range(n):
    threading.Thread(target=fd).start()
