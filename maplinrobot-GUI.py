#!/usr/bin/env python

#ROBOT ARM CONTROL PROGRAM

# MoveArm(1,[0,1,0]) @Rotate base anti-clockwise
# MoveArm(1,[0,2,0]) @Rotate base clockwise
# MoveArm(1,[64,0,0]) @Shoulder up
# MoveArm(1,[128,0,0]) @Shoulder down
# MoveArm(1,[16,0,0]) @Elbow up
# MoveArm(1,[32,0,0]) @Elbow down
# MoveArm(1,[4,0,0]) @Wrist up
# MoveArm(1,[8,0,0]) @ Wrist down
# MoveArm(1,[2,0,0]) @Grip open
# MoveArm(1,[1,0,0]) @Grip close
# MoveArm(1,[0,0,1]) @Light on
# MoveArm(1,[0,0,0]) @Light off

#Use sudo pip install pyusb for usb.core

from Tkinter import *
from ttk import *
import random
import usb.core, usb.util, time, sys

class App:
	def __init__(self, master):
		
		self.usb_vendor_id=0x1267
		self.usb_prod_id=0x000
		self.rctl = usb.core.find(idVendor=self.usb_vendor_id, idProduct=self.usb_prod_id) #Object to talk to the robot
		self.duration=1.0 # Duration (In seconds) for each action. Defaults to 1 second
		

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
		
		def abrir (self):
			self.MoveArm(t=1, cmd='abrir-pinza')
			
		#---------------Ambiente Grafico- -----------#
		mainframe = Frame(master, padding = '3 3 12 12')
		#hace que el marco se empaquete en el espacio disponible
	
		mainframe.grid(column=0, row= 0, sticky=(N,W,E,S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)
		
		
		#variables
		self.tiempo = DoubleVar()
		self.ordenesGrabadas=[]
		self.enGrabacion=False
		
		
		#pinza
		Label(mainframe, text='Pinza').grid(column=0, row=0, sticky=W)
		Button(mainframe, text="Abrir", command = self.abrir ).grid(column=1, row=0, sticky=W)
		Button(mainframe, text="Cerrar", command = self.cerrar).grid(column=1, row=1, sticky=W)
		
		#separador verticales
		Label(mainframe, text='     ').grid(column=2, row=1, sticky=W)
		
		#base
		Label(mainframe, text='Base').grid(column=3, row=0, sticky=E)
		Button(mainframe, text="derecha", command = self.baseDerecha ).grid(column=4, row=0, sticky=W)
		Button(mainframe, text="izquierda", command = self.baseIzquierda).grid(column=4, row=1, sticky=W)
		
		#separador vertical
		Label(mainframe, text='     ').grid(column=5, row=1, sticky=W)

		#hombro
		Label(mainframe, text='Hombro').grid(column=6, row=0, sticky=E)
		Button(mainframe, text="subir", command = self.subirHombro).grid(column=7, row=0, sticky=W)
		Button(mainframe, text="bajar", command = self.bajarHombro).grid(column=7, row=1, sticky=W)
		
		#codo
		Label(mainframe, text='Codo').grid(column=0, row=4, sticky=W)
		Button(mainframe, text="subir", command = self.subirCodo).grid(column=1, row=4, sticky=W)
		Button(mainframe, text="bajar", command = self.bajarCodo).grid(column=1, row=5, sticky=W)
		
		#munneca
		Label(mainframe, text='Munneca').grid(column=3, row=4, sticky=W)
		Button(mainframe, text="subir", command = self.subirMunneca).grid(column=4, row=4, sticky=W)
		Button(mainframe, text="bajar", command = self.bajarMunneca).grid(column=4, row=5, sticky=W)
		
		#separador horizontal
		Label(mainframe, text=' ').grid(column=3, row=3, sticky=W)
		
		#luz
		Label(mainframe, text='Luz').grid(column=6, row=4, sticky=E)
		Button(mainframe, text="encender", command = self.encenderLuz).grid(column=7, row=4, sticky=W)
		Button(mainframe, text="apagar", command = self.apagarLuz).grid(column=7, row=5, sticky=W)
		
		#grabacion
		Label(mainframe, text='Grabacion').grid(column=0, row=8, sticky=W)
		Button(mainframe, text="Play", command = self.ejecutarOrdenesGrabadas).grid(column=0, row=9, sticky=W)
		Button(mainframe, text="Grabar", command = self.iniciarGrabacion).grid(column=1, row=9, sticky=W)
		
		Label(mainframe, text='Estado Grabacion').grid(column=0, row=10, sticky=W)
		
		#ordenes
		Label(mainframe, text='ordenes').grid(column=7, row=7, sticky=W)
		message = Message(mainframe, text=str([orden[0] for orden in self.ordenesGrabadas]))
		message.grid(row=8,column=7, sticky=E)

		#separador horizontal
		Label(mainframe, text='    ').grid(column=0, row=5, sticky=W)
		
		#tiempo deslizable
		Label(mainframe, text='Tiempo').grid(column=0, row=6, sticky=W)
		scale=Scale(mainframe, from_=1, to=4, orient=HORIZONTAL,
			command=self.onScale).grid(column=0, row=7)
		Label(mainframe, textvariable=self.tiempo,
			font=("Helvetica", 15)).grid(row=7, column=1,sticky=E)
			
	def onScale(self, val):
		v = int(float(val))
		self.tiempo.set(v)
		
	
	def iniciarGrabacion(self):
		self.enGrabacion=True
		
	
				
		
		
		
	def abrir (self):
		self.MoveArm(t=self.tiempo.get(), cmd='abrir-pinza')
		if self.enGrabacion:
			self.ordenesGrabadas.append(('abrir-pinza', self.tiempo.get()))
	
	def cerrar (self):
		self.MoveArm(t=1, cmd='cerrar-pinza')	
		if self.enGrabacion:
			self.ordenesGrabadas.append(('cerrar-pinza', self.tiempo.get()))
		
	def baseDerecha (self):
		self.MoveArm(t=self.tiempo.get(), cmd='base-derecha')
		if self.enGrabacion:
			self.ordenesGrabadas.append(('base-derecha', self.tiempo.get()))
		
	def baseIzquierda (self):
		self.MoveArm(t=self.tiempo.get(), cmd='base-izquierda')
		if self.enGrabacion:
			self.ordenesGrabadas.append(('base-izquierda', self.tiempo.get()))
		
	def subirHombro (self):
		self.MoveArm(t=self.tiempo.get(), cmd='subir-hombro')
		if self.enGrabacion:
			self.ordenesGrabadas.append(('subir-codo', self.tiempo.get()))	
		
	def bajarHombro (self):
		self.MoveArm(t=self.tiempo.get(), cmd='bajar-hombro')
		if self.enGrabacion:
			self.ordenesGrabadas.append(('bajar-hombro', self.tiempo.get()))
		
	def subirCodo(self):
		self.MoveArm(t=self.tiempo.get(), cmd='subir-codo')
		
	def bajarCodo (self):
		self.MoveArm(t=self.tiempo.get(), cmd='bajar-codo')
		
	def subirMunneca(self):
		self.MoveArm(t=self.tiempo.get(), cmd='subir-munneca')
		
	def bajarMunneca (self):
		self.MoveArm(t=self.tiempo.get(), cmd='bajar-munneca')
		
	def encenderLuz (self):
		self.MoveArm(t=self.tiempo.get(), cmd='encender-luz')
		
	def apagarLuz (self):
		self.MoveArm(t=self.tiempo.get(), cmd='apagar-luz')
		

	
	def ejecutarOrdenesGrabadas(self):
		print self.ordenesGrabadas
		print self.enGrabacion
		for orden in self.ordenesGrabadas:
			self.tiempo.set(orden[1])
			if orden[0]=='encender-luz':
				self.encenderLuz()
			elif orden[0]=='apagar-luz':
				apagarLuz()
			elif orden[0]=='abrir-pinza':
				self.abrir()
			elif orden[0]=='cerrar-pinza':
				self.cerrar()
			elif orden[0]=='base-derecha':
				self.baseDerecha()
			elif orden[0]=='base-izquierda':
				self.baseIzquierda()
			elif orden[0]=='subir-hombro':
				self.subirHombro()
			elif orden[0]=='bajar-hombro':
				self.bajarHombro()
			elif orden[0]=='subir-codo':
				self.subirCodo()
			elif orden[0]=='bajar-codo':
				self.bajarCodo()
			elif orden[0]=='subir-munneca':
				self.subirMunneca()
			elif orden[0]=='bajar-munneca':
				self.bajarMunneca()
			else:
				pass
				
					
			
				
			

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
			print "USB error de comunicacion.\n"
			return False

	def MoveArm(self,t,cmd):
		print self.ordenesGrabadas
		print self.enGrabacion
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
			print "USB error de comunicacion.\n"
			return False
			
		
	
		
root=Tk()
root.title ('maplinRobot Arm')
app=App(root)
root.mainloop()






# ejemplo de uso con teclas
#s = MaplinRobot()

#enCalibracion = False


#while True:
	#if enCalibracion:
		#print "ATENCION ESTA USTED CALIBRANDO"
		#print "vease la foto ubicada en la carpeta del brazo"
		#print "para ver como colocar el brazo en la calibracion"
		#print ""
	#print """pulsa '1' para encender la luz, 'a' para girar la base hacia  la derecha, 'd' para girar la base hacia la izquierda"""
	#print """pulsa 'w' para subir el hombro y 's' para bajarlo """
	#print """pulsa 'r' para subir el codo y 'f' para bajarlo"""
	#print """pulsa 't' para subir la munneca o 'g' para bajarla"""
	#print """pulsa 'y' para abrir pinza o 'h' para cerrarla"""
	#print """para salir del programa pulsar la tecla "p" """
	#print """pulsa "c" para empezar a calibrar y "v" para terminar de calibrar"""
	#print ""
	#s.MostrarPosiciones() 
	#tiempo = 1.00
	
	#orden = raw_input()
	#if orden == "c":
		
		#enCalibracion = True
	#elif orden == "v":
		#s.posiciones ["base"]=0
		#s.posiciones ["hombro"]=0
		#s.posiciones ["codo"]=16
		#s.posiciones ["munneca"]=0
		#s.posiciones ["pinza"]=0
		#enCalibracion = False
	#elif orden == "1":
		#s.MoveArm(t=5.0, cmd='encender-luz')
	#elif orden == "a" and (enCalibracion or s.posiciones ["base"] < 15):
		#s.MoveArm(t=tiempo, cmd='base-derecha')
		#s.posiciones ["base"] += tiempo
	#elif orden == "d" and (enCalibracion or s.posiciones ["base"] > 1):
		#s.MoveArm(t=tiempo, cmd='base-izquierda')
		#s.posiciones ["base"] -= tiempo
	#elif orden == "w" and (enCalibracion or s.posiciones ["hombro"] < 12):
		#s.MoveArm(t=tiempo, cmd='subir-hombro')
		#s.posiciones["hombro"] += tiempo
	#elif orden == "s" and (enCalibracion or s.posiciones ["hombro"] > 1):
		#s.MoveArm(t=tiempo, cmd='bajar-hombro')
		#s.posiciones["hombro"] -= tiempo
	#elif orden == "r" and (enCalibracion or s.posiciones ["codo"] < 16):
		#s.MoveArm(t=tiempo, cmd='subir-codo')
		#s.posiciones["codo"] += tiempo
	#elif orden == "f" and (enCalibracion or s.posiciones ["codo"] > 1):
		#s.MoveArm(t=tiempo, cmd='bajar-codo')
		#s.posiciones["codo"] -= tiempo
	#elif orden == "t" and (enCalibracion or s.posiciones ["munneca"] < 7):
		#s.MoveArm(t=tiempo, cmd='subir-munneca')
		#s.posiciones["munneca"] += tiempo
	#elif orden == "g" and (enCalibracion or s.posiciones ["munneca"] > 1):
		#s.MoveArm(t=tiempo, cmd='bajar-munneca')
		#s.posiciones["munneca"] -= tiempo
	#elif orden == "y" and (enCalibracion or s.posiciones ["pinza"] < 3):
		#s.MoveArm(t=tiempo/4.0, cmd='abrir-pinza')
		#s.posiciones["pinza"] += tiempo
	#elif orden == "h" and (enCalibracion or s.posiciones ["pinza"] > 0):
		#s.MoveArm(t=tiempo/4.0, cmd='cerrar-pinza')
		#s.posiciones["pinza"] -= tiempo
	#elif orden == "p":
		#print "esto es todo por hoy"
		#break
		
	#else:
		#print "no has pulsado la tecla correcta"
	





