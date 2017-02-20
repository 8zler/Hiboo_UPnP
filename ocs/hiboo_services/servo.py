from twisted.internet import reactor
from pyupnp.event import EventProperty
from pyupnp.device import Device, DeviceIcon
from pyupnp.services import register_action, Service, ServiceActionArgument, ServiceStateVariable
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
import grovepi,os,glob,time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')





class ServoService(Service):

	version = (1, 0)
	serviceType = "urn:schemas-upnp-org:service:ServoSercice:1"
	serviceId = "urn:upnp-org:serviceId:ServoSercice"

	actions = {
		'TurnServo': [
			ServiceActionArgument('angle','in','angle'),
                        ServiceActionArgument('finished','out','finished')
		]
	}
	
	stateVariables = [
		ServiceStateVariable('angle','string',sendEvents=True),	
		ServiceStateVariable('ListeningServo','boolean',sendEvents=True),
                ServiceStateVariable('finished','boolean',sendEvents=True)

	]
		
	state=EventProperty('ListeningServo')
	angle=EventProperty('angle')
	finished=EventProperty('finished',False)

	@register_action('TurnServo')
	def turnS(self,arg):
		if(int(arg) > 250 or int(arg) < 50):
			return
		if(int(arg)==50):
			os.system("echo 0="+str(arg)+" > /dev/servoblaster")
			time.sleep(1)
			os.system("echo 0="+str(0)+" > /dev/servoblaster")
		else:
			os.system("echo 0="+str(arg)+" > /dev/servoblaster")
		time.sleep(1)
		if self.finished == True:
			return {
				'finished': False
				}
		if self.finished == False:
			return {
				'finished': True
			}

