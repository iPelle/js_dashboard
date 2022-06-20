# https://stackoverflow.com/questions/68033119/get-data-from-a-dropdown-menu-with-fastapi
import json
import asyncio
from fastapi import FastAPI, Form, File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
from enum import Enum
from google.cloud import pubsub_v1


app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="templates")

'''
with open('measurements.json', 'r') as file:
    measurements = iter(json.loads(file.read()))
'''

# TO TO
# Implement all_sensors2

with open('sample.json', 'r') as file:
    measurements = iter(json.loads(file.read()))

'''
all_sensors = {'Machine_1': ['Sensor_11', 'Sensor_12', 'Sensor_13'],
				'Machine_2': ['Sensor_21', 'Sensor_22', 'Sensor_23']}
'''
all_sensors = {'Dummy machine': None}
current_machine = None

def update_sensors(payload):
	machine = payload['deviceId']
	sensor = payload['Name']
	added = ''
	if machine not in all_sensors.keys():
		all_sensors[machine] = []
		#added += added + " added machine: " +machine
		print(machine)
	if sensor not in all_sensors[machine]:
		all_sensors[machine].append(sensor)
		#added += added + " added sensor: " +sensor
		print(sensor)
	#print('All sensors:')
	#print(all_sensors)
	return


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.01)
        payload = next(measurements)
        await websocket.send_json(payload)
        update_sensors(payload)


# --------------------------------------------

# Prova dropdown_upload (multiselect)
# --------------------------------------------

# First page load
@app.get('/dropdown_multiselect')
def upload(request: Request):
    return templates.TemplateResponse('dropdown_multiselect.html', context={'request': request, 'all_machines': list(all_sensors.keys())})
    # Gets data from upload.html

# When sensors are selected
@app.post("/dropdown_multiselect")
async def handle_form(request: Request,
                      selected_machine: str = Form(...),
                      selected_sensors: list = Form(...)
                      ):
    
    global current_machine

    current_machine = selected_machine
    
    context = {'request': request,'all_machines': list(all_sensors.keys())}
    has_selected_machine = all_sensors.get(current_machine)
    
    # Check if there is a selected machine
    if(has_selected_machine is not None):
    	context['selected_machine'] = selected_machine
    	if(len(has_selected_machine) > 0):
    		context['all_sensors'] = all_sensors.get(current_machine)

    if(len(selected_sensors)>0):
    	context['selected_sensors'] = selected_sensors
 
    return templates.TemplateResponse('dropdown_multiselect.html', context=context)




'''
# When machine is selected
@app.post("/select_machine")
async def handle_form(request: Request,
                      selected_machine: str = Form(...)
                      ):
    print(selected_machine)
    global current_machine
    current_machine = selected_machine
    return templates.TemplateResponse('dropdown_multiselect.html', context={'request': request,
                                                              'all_machines': list(all_sensors.keys()),
                                                              'all_sensors': all_sensors.get(current_machine)})

# When sensors are selected
@app.post("/select_sensors")
async def handle_form(request: Request,
                      selected_sensors: list = Form(...)
                      ):
    print(selected_sensors)
    print("this might be wrong...")
    print(all_sensors.get(current_machine))
    print("this is the machine")
    print(current_machine)
    return templates.TemplateResponse('dropdown_multiselect.html', context={'request': request,
                                                              'all_machines': list(all_sensors.keys()),
                                                              'all_sensors': all_sensors.get(current_machine)})

# --------------------------------------------


# --------------------------------------------
'''


