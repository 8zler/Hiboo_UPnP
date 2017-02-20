# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Doc & examples : https://github.com/fuzeman/PyUPnP

from twisted.internet import reactor
from pyupnp.event import EventProperty
from pyupnp.device import Device, DeviceIcon
from pyupnp.services import register_action, Service, ServiceActionArgument, ServiceStateVariable
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
from hiboo_services.detection import DetectionService
from hiboo_services.filemanager import FileManageService
from hiboo_services.servo import ServoService
from hiboo_services.CameraManager import CameraService
import time,random,os



class HibooDevice(Device):
    deviceType = 'urn:schemas-upnp-org:device:Hiboo:1'
    friendlyName = "HibooTrackersssss"
    
    def __init__(self):
        Device.__init__(self)
        self.uuid='3a34765e-5e91-4627-b735-1041eaf49740'

        self.detect = DetectionService()
        self.fileM = FileManageService()
        self.servo = ServoService()
	self.cam = CameraService()

        
        self.services = [
            self.detect,
            self.fileM,
            self.servo,
            self.cam,
        ]

        
        self.icons = [DeviceIcon('image/png', 32, 32, 24,'./hiboo.png')]

        
if __name__ == '__main__':

    device = HibooDevice()

    upnp = UPnP(device)
    ssdp = SSDP(device)

    upnp.listen()
    ssdp.listen()

    print "Hiboooo trackersss online"

    reactor.run()
    
        
