import usb.core, usb.util, time, sys
#Use sudo pip install pyusb for usb.core

class comunicacion:
	def __init__(self):
		
		self.moves={
		'base-izquierda' : [0,1,0],
		'base-derecha' : [0,2,0],
		'subir-hombro': [64,0,0],
		'bajar-hombro': [128,0,0],
		'subir-codo': [16,0,0],
		'bajar-codo': [32,0,0],
		'subir-munneca': [4,0,0],
		'bajar-munneca': [8,0,0],
		'abrir-pinza': [2,0,0],
		'cerrar-pinza': [1,0,0],
		'encender-luz': [0,0,1],
		'apagar-luz': [0,0,0],
		'parar': [0,0,0],
		}

		self.usb_vendor_id=0x1267
		self.usb_prod_id=0x000
		self.rctl = usb.core.find(idVendor=self.usb_vendor_id, idProduct=self.usb_prod_id) #Object to talk to the robot
	
	def SetVendorId(self,vid):
		self.usb_vendor_id = vid


	def SetProdID(self,pid):
		self.usb_prod_id = pid


	def StopArm(self):
		if self.CheckComms():
			self.rctl.ctrl_transfer(0x40,6,0x100,0,self.moves['parar'],1000) #Send stop command	
			return True
		else:
			return False


	def CheckComms(self):
		'''Checks that the arm is connected and we can talk to it'''
		try:
			if self.rctl != None:
				return True
			else:
				print "no se puede comunicar con el brazo.\n"
				return False
		except usb.core.USBError:
			print "USB error de comunicacion 1 .\n"
			return False

	def MoveArm(self,t,cmd):
		
		try:
			#Check that we can send commands to the arm
			if self.CheckComms():
				#We can send stuff
				print "enviando comando %s\n" %cmd
				self.rctl.ctrl_transfer(0x40,6,0x100,0,self.moves[cmd],1000) #Send command
				time.sleep(t) #Wait 
				self.StopArm()
				print "hecho.\n"
				return True
			else:
				return False
			
		except KeyboardInterrupt:
			print "ctrl-c presionado. parando el brazo"
			self.StopArm()
			return False

		except usb.core.USBError:
			print "USB error de comunicacion 2.\n"
			return False
