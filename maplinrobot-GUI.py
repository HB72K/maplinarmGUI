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

from comunicacion_con_brazo import comunicacion

class App:
	def __init__(self, master):
		"""iniciando la comunicacion con el brazo"""
		self.com=comunicacion()
		
		"""inicio de ambiente grafico"""
		
		self.duration=1.0 # Duration (In seconds) for each action. Defaults to 1 second
		

		
		
			
		#---------------Ambiente Grafico- -----------#
		mainframe = Frame(master, padding = '3 3 12 12')
		#hace que el marco se empaquete en el espacio disponible
	
		mainframe.grid(column=0, row= 0, sticky=(N,W,E,S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)
		
		
		# ---------------------- Variables -------------------------
		self.tiempo = DoubleVar()
		self.ordenesGrabadas=[]		#("base-izquierda", 1), ("base-derecha",1)
		self.cadenaOrdenes=""
		self.numeroOrdenes=0
		self.ordenesGrabadasString=StringVar()
		self.enGrabacion=BooleanVar()
		
		
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
		
		Label(mainframe, text='Estado Grabacion ').grid(column=0, row=10, sticky=W)
		Label(mainframe, textvariable=self.enGrabacion).grid(column=0, row=11, sticky=W)

		
		#ordenes
		Label(mainframe, text='ordenes').grid(column=7, row=7, sticky=W)
		message = Message(mainframe, textvariable=self.ordenesGrabadasString)
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
		"""ajusta el valor del tiempo mediante barra deslizante"""
		v = int(float(val))
		self.tiempo.set(v)
		
	
	def iniciarGrabacion(self):
		self.enGrabacion.set(True)
		
	def pararGrabacion(self):
		self.enGrabacion.set(False)
	
	def actualizarOrdenesGrabadas(self,comando):
		""" Esta funcion por ahora no es muy elegante: hace dos cosas a la vez """
		self.ordenesGrabadas.append((comando, self.tiempo.get()))
		cont=0
		for orden in self.ordenesGrabadas[self.numeroOrdenes:]:
			self.cadenaOrdenes += orden[0] + " "
			cont+=1
		self.numeroOrdenes+=cont
		self.ordenesGrabadasString.set(self.cadenaOrdenes)
		print self.cadenaOrdenes

	def abrir (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='abrir-pinza')
		if self.enGrabacion.get():
			self.actualizarOrdenesGrabadas('abrir-pinza')
	
	def cerrar (self):
		self.com.MoveArm(t=1, cmd='cerrar-pinza')	
		if self.enGrabacion.get():
			self.actualizarOrdenesGrabadas('cerrar-pinza')
		
	def baseDerecha (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='base-derecha')
		if self.enGrabacion.get():
			self.actualizarOrdenesGrabadas('base-derecha')
		
	def baseIzquierda (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='base-izquierda')
		if self.enGrabacion.get():
			self.actualizarOrdenesGrabadas('base-izquierda')
		
	def subirHombro (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='subir-hombro')
		if self.enGrabacion.get():	
			self.actualizarOrdenesGrabadas('subir-hombro')
		
	def bajarHombro (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='bajar-hombro')
		if self.enGrabacion.get():
			self.actualizarOrdenesGrabadas('bajar-hombro')
	
	#aniadir funcion enGrabacion desde subirCodo hasta apagarLuz	
	def subirCodo(self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='subir-codo')
		
	def bajarCodo (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='bajar-codo')
		
	def subirMunneca(self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='subir-munneca')
		
	def bajarMunneca (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='bajar-munneca')
		
	def encenderLuz (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='encender-luz')
		
	def apagarLuz (self):
		self.com.MoveArm(t=self.tiempo.get(), cmd='apagar-luz')
		

	
	def ejecutarOrdenesGrabadas(self):
		self.pararGrabacion()
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
				
					
	
			
		
	
		
root=Tk()
root.title ('maplinRobot Arm')
app=App(root)
root.mainloop()







	





