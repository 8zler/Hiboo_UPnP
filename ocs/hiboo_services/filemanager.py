from twisted.internet import reactor
from pyupnp.event import EventProperty
from pyupnp.device import Device, DeviceIcon
from pyupnp.services import register_action, Service, ServiceActionArgument, ServiceStateVariable
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
import grovepi,os,glob,time,base64
from random import randint

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')





def read_dir(path):
	try:
		res = []
		for file in glob.glob(path+"*.*"):
			res.append(str(file.split("/")[-1]))
		res.sort()
		ret = ";".join(res)
		return ret

	except IOError:
		return "Error dir"

class FileManageService(Service):

	version = (1, 0)
	serviceType = "urn:schemas-upnp-org:service:FileManageService:1"
	serviceId = "urn:upnp-org:serviceId:FileManageService"

	actions = {
		'ScanDir': [
			ServiceActionArgument('scan_ret','out','scan_ret')
		],
		'GetPicture': [
			ServiceActionArgument('path','in','path'),
			ServiceActionArgument('data','out','data')
		],
		'DeleteFile': [
			ServiceActionArgument('fileToDelete','in','fileToDelete')
		]
	}
	
	stateVariables = [
		ServiceStateVariable('allFile','string',sendEvents=True),
		ServiceStateVariable('path','string',sendEvents=True),
		ServiceStateVariable('ListeningDir','string',sendEvents=True),
		ServiceStateVariable('data','string',sendEvents=True),
		ServiceStateVariable('scan_ret','string',sendEvents=True),
		ServiceStateVariable('fileToDelete','string',sendEvents=True)

	]
		
	state=EventProperty('ListeningDir')
	string=EventProperty('allFile')
	data=EventProperty('data')
	deletedFile=EventProperty('fileToDelete')
	

	@register_action('ScanDir')
	def scanD(self):
		self.r=1
		self.r+=1
		print "IN SCAN DIR"
		#self.string = str(read_dir("/home/pi/PICTURE_FROM_HIBOO/"))
		return {
			'scan_ret' : str(read_dir("/home/pi/PICTURE_FROM_HIBOO/"))
		}

	

	@register_action('GetPicture')
	def getPicture(self,arg):
		print "IN GET PICTURE: "+str(arg)
		with open("/home/pi/PICTURE_FROM_HIBOO/"+str(arg), "rb") as self.imageFile:
			#self.imageFile = open(str(arg), "rb")
			self.res = base64.b64encode(self.imageFile.read())
			print(len(self.res))
	    		print("decode done")
	    		self.fh = open("imageToSave.png", "wb")
	    		self.fh.write(base64.b64decode(self.res))
	    		self.fh.close()
		return {
			'data': self.res # base64.b64encode(open(str(arg), "rb").read())
		}

	@register_action('DeleteFile')
	def empty(self,arg):
		print("IN DELETE FILE : "+str(arg))
		self.folder = "/home/pi/PICTURE_FROM_HIBOO"
		os.remove(self.folder+"/"+arg)
		

