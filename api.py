from flask import Flask, request
from collections import Iterable
import json
app = Flask(__name__)


'''
battery configuration and inventory configuration is not clear in pdf , so consider this 

'''


#GET REQUEST
#POST REQUEST ENVIRONMENT
@app.route('/api/environment/configure', methods = ['POST'])
def postRequestEnvironment():
    
    content=request.json
    data=json.dumps(content)
    with open('api_environment_configure.txt','w') as write_file:
        json.dump(data,write_file)
    return "Evironment configure is successfully done with post"


#UPDATE REQUEST
@app.route('/api/environment', methods = ['PATCH'])
def patchRequestEnvironment():
    content=request.json
    with open('api_environment_configure.txt','r') as read_file:
        dict_data=json.load(read_file)
        if(type(dict_data)==str):
               dict_data=json.loads(dict_data)
            
        for x, y in dict_data.items():
            for i,j in content.items():
                if x==i:
                    dict_data[x]=j
                else:
                    return i + " not present in environment"
                    
        with open('api_environment_configure.txt','r+') as read_erase:
            read_erase.truncate()
        with open('api_environment_configure.txt','w') as write_file:
            json.dump(dict_data,write_file)
    return "envirnment PATCH request is succesfully done"


#POST REQUEST ROVER
@app.route('/api/rover/configure', methods=['POST'])
def postRequestRover():
    content=request.json
    data=json.dumps(content)
    with open('api_rover_configure.txt','w') as write_file:
        json.dump(data, write_file)
        
    return "roven configure is successfulil done with post"    


@app.route('/api/rover/move', methods=['POST'])
def postRequestRoverMove():
    content=request.json
    data=json.dumps(content)
    dict_data= json.loads(data)
    directions=['up','down','left','right']
    if(dict_data['direction'] in directions):
        with open('api_environment_configure.txt','r') as read_file:
            dict_data=json.load(read_file)
            if(type(dict_data)==str):
               dict_data=json.loads(dict_data)
            
            if(dict_data['storm']==True):
                return "Cannot move during a storm"
            else:
                return "OK status"
    else:
        return "Invalid direction"
        
        

@app.route('/api/rover/status')
def getRequestRoverStatus():
    
    with open('api_rover_configure.txt','r') as read_file:
        data=json.load(read_file)
        dict_data=json.loads(data)
        new_rover_status={}
        new_rover_status['rover']={}
        new_rover_status['rover']['location']=dict_data['deploy-point']
        new_rover_status['rover']['inventory']=dict_data['inventory']
        new_rover_status['rover']['battery']=dict_data['initial-battery']
                
        with open('api_environment_configure.txt','r') as r:
           data2= json.load(r)
           if(type(data2)==str):
               data2=json.loads(data2)
           
           a=list(flatten(data2['area-map']))
           b=(list(dict.fromkeys(a)))
           data2.pop('area-map')
           data2['terrain']=b[0]
           new_rover_status['rover']['environment']=data2
 
                 
    return new_rover_status
      

def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item            
        

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)  