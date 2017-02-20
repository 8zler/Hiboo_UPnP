from twisted.internet import reactor
from pyupnp.event import EventProperty
from pyupnp.device import Device, DeviceIcon
from pyupnp.services import register_action, Service, ServiceActionArgument, ServiceStateVariable
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
import grovepi,os,glob,time,picamera,shutil,datetime
from random import randint

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

camera=picamera.PiCamera()

def takePicture():
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
        time.sleep(5)
	print("PICTURE CREATED ON FOLDER")
        camera.capture("/home/pi/PICTURE_FROM_HIBOO/"+str(st) + '.jpg')



class CameraService(Service):

	version = (1, 0)
	serviceType = "urn:schemas-upnp-org:service:CameraService:1"
	serviceId = "urn:upnp-org:serviceId:CameraService"

	actions = {
		'TakePicture': [
			ServiceActionArgument('take','out','take')
		]
	}
	
	stateVariables = [
		ServiceStateVariable('take','boolean',sendEvents=True),	
		ServiceStateVariable('ListeningCamera','boolean',sendEvents=True)

	]
		
	state=EventProperty('ListeningCamera')
	take=EventProperty('take',False)

        #camera = picamera.PiCamera()



	@register_action('TakePicture')
	def takeP(self):
		print "IN TAKE PICTURE"
		takePicture()
		return{
                        'take': True
                }


