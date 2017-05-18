"""
just to start wsn and dispatcher 

later can be expanded to get status from dispatcher and wsn

"""



import subprocess,sys,json

def start(app_name):
    f=open('config/'+app_name+'.txt','r') # opens app config
    app_config=json.loads(f.read())
    f.close()
    subprocess.Popen(['python','dispatcher.py',app_config['app_name']]) # starts dispatcher and sends app name to dispatcher
    subprocess.Popen(['python','wsn.py',str(app_config['port']),app_config['app_name']]) # starts wsn manager and sends app name and port to listen 







if __name__=='__main__':
    app_name=sys.argv[1] #receives app name from fog
    start(app_name)
