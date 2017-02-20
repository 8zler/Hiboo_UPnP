from twisted.internet import reactor
from pyupnp.event import EventProperty
from pyupnp.device import Device, DeviceIcon
from pyupnp.logr import Logr
from pyupnp.services import register_action, Service, ServiceActionArgument, ServiceStateVariable
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
import grovepi,os,glob,time
from random import randint

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


pir_sensor1 = 5
pir_sensor2 = 2
pir_sensor3 = 8

grovepi.pinMode(pir_sensor1, "INPUT")
grovepi.pinMode(pir_sensor2, "INPUT")
grovepi.pinMode(pir_sensor3, "INPUT")

motion1 = 0
motion2 = 0
motion3 = 0




def read_sensor(pir_sensorX):
	try:
		sensor_value = grovepi.digitalRead(pir_sensorX)
		if sensor_value == 1:
			return True
		else:
			return False
	except IOError:
		return "Error sensor"

class DetectionService(Service):

	version = (1, 0)
	serviceType = "urn:schemas-upnp-org:service:SensorService:1"
	serviceId = "urn:upnp-org:serviceId:SensorService"

	actions = {
		'setDetect': [
			ServiceActionArgument('detectOrNot','in','detectOrNot')
		]
	}
	
	stateVariables = [
		ServiceStateVariable('sensor1','boolean',sendEvents=True),
		ServiceStateVariable('sensor2','boolean',sendEvents=True),
		ServiceStateVariable('sensor3','boolean',sendEvents=True),
                ServiceStateVariable('detectOrNot','boolean',sendEvents=True),
		ServiceStateVariable('ListeningSensor','boolean',sendEvents=True)

	]
		
	state=EventProperty('ListeningSensor')
	sen1=EventProperty('sensor1',False)
	sen2=EventProperty('sensor2',False)
	sen3=EventProperty('sensor3',False)

	@register_action('setDetect')
	def setD(self,arg):
                print arg,type(arg),bool(int(arg))
                print "setDetect called"
                self.sen1 = False
                self.sen2 = False
                self.sen3 = False
                while bool(int(arg)):
                        print "setDetect : in while"
                        self.m1=read_sensor(pir_sensor1)
                        self.m2=read_sensor(pir_sensor2)
                        self.m3=read_sensor(pir_sensor3)
                        print self.m1,self.m2,self.m3
                        if self.m1 == True:
                                self.sen1 = self.m1
                                break
                        if self.m2 == True:
                                self.sen2 = self.m2
                                break
                        if self.m3 == True:
                                self.sen3 = self.m3
                                break
                print "setDetect end"		

