from socket import *
import time
import threading


def ff(n):
    s=socket()
    dat=str(n)
    iD='S'+str(n)
    msg='pub:'+iD
    s.connect(('127.0.0.1',4321))
    s.sendall(msg.encode('utf-8'))
    time.sleep(0.1)
    while True:
          msg=iD+':'+dat
          s.sendall(msg.encode('utf-8'))
          time.sleep(1)


if __name__=='__main__':
    for i in range(10):
        threading.Thread(target=ff,args=(i,)).start()
        time.sleep(1)
        