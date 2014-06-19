#!/usr/bin/env python

from Tkinter import *
from ttk import *
import random

from comunicacion_con_brazo import comunicacion

class App:
	def __init__(self, master):
		"""iniciando la comunicacion con el brazo"""
		self.com=comunicacion()
		
		# ---------------------- Variables -------------------------
		self.master = master
		self.tiempo = DoubleVar()
		self.ordenesGrabadas=[]		#Ejemplo: ordenesGrabadas=[("base-izquierda", 1), ("base-derecha",1)]
		self.cadenaOrdenes=""
		self.ordenesGrabadasString=StringVar()
		self.enGrabacion=BooleanVar()
		self.duration=1.0 # Duration (In seconds) for each action. Defaults to 1 second
		
		#---------------Ambiente Grafico- -----------#
		mainframe = Frame(master, padding = '3 3 12 12')
		#hace que el marco se empaquete en el espacio disponible
	
		mainframe.grid(column=0, row= 0, sticky=(N,W,E,S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)
		
		#pinza
		Label(mainframe, text='Pinza').grid(column=0, row=0, sticky=W)
		Button(mainframe, text="Abrir", command = lambda : self.actuar('abrir-pinza') ).grid(column=1, row=0, sticky=W)
		Button(mainframe, text="Cerrar", command = lambda : self.actuar('cerrar-pinza')).grid(column=1, row=1, sticky=W)
		
		#separador verticales
		Label(mainframe, text='     ').grid(column=2, row=1, sticky=W)
		
		#base
		Label(mainframe, text='Base').grid(column=3, row=0, sticky=E)
		Button(mainframe, text="derecha", command = lambda : self.actuar('base-derecha') ).grid(column=4, row=0, sticky=W)
		Button(mainframe, text="izquierda", command = lambda : self.actuar('base-izquierda')).grid(column=4, row=1, sticky=W)
		
		#separador vertical
		Label(mainframe, text='     ').grid(column=5, row=1, sticky=W)
	
		#hombro
		Label(mainframe, text='Hombro').grid(column=6, row=0, sticky=E)
		Button(mainframe, text="subir", command = lambda : self.actuar('subir-hombro')).grid(column=7, row=0, sticky=W)
		Button(mainframe, text="bajar", command = lambda : self.actuar('bajar-hombro')).grid(column=7, row=1, sticky=W)
		
		#codo
		Label(mainframe, text='Codo').grid(column=0, row=4, sticky=W)
		Button(mainframe, text="subir", command = lambda : self.actuar('subir-codo')).grid(column=1, row=4, sticky=W)
		Button(mainframe, text="bajar", command = lambda : self.actuar('bajar-codo')).grid(column=1, row=5, sticky=W)
		
		#munneca
		Label(mainframe, text='Munneca').grid(column=3, row=4, sticky=W)
		Button(mainframe, text="subir", command = lambda : self.actuar('subir-munneca')).grid(column=4, row=4, sticky=W)
		Button(mainframe, text="bajar", command = lambda : self.actuar('bajar-munneca')).grid(column=4, row=5, sticky=W)
		
		#separador horizontal
		Label(mainframe, text=' ').grid(column=3, row=3, sticky=W)
		
		#luz
		Label(mainframe, text='Luz').grid(column=6, row=4, sticky=E)
		Button(mainframe, text="encender", command = lambda : self.actuar('encender-luz')).grid(column=7, row=4, sticky=W)
		Button(mainframe, text="apagar", command = lambda : self.actuar('apagar-luz')).grid(column=7, row=5, sticky=W)
		
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
					
	# ---------------------- Acciones -------------------------	
	def onScale(self, val):
		"""ajusta el valor del tiempo mediante barra deslizante"""
		v = int(float(val))
		self.tiempo.set(v)
	
	def actuar(self, comando):
		""" Envia el comando de movimiento al brazo y graba la orden si 
		self.enGrabacion es True """
		self.com.MoveArm(t=self.tiempo.get(), cmd=comando)
		if self.enGrabacion.get():
			self.actualizarOrdenesGrabadas(comando)
			
	
	# -----------------------------------------------------------	
	# Proceso de grabacion de ordenes y ejecucion de las mismas
	# -----------------------------------------------------------
	
	def iniciarGrabacion(self):
		self.enGrabacion.set(True)
		
	def pararGrabacion(self):
		self.enGrabacion.set(False)
	
	def actualizarOrdenesGrabadas(self,comando):
		self.ordenesGrabadas.append((comando, self.tiempo.get()))
		self.cadenaOrdenes += comando + "\n"
		self.ordenesGrabadasString.set(self.cadenaOrdenes)
		print self.cadenaOrdenes
	
	def ejecutarOrdenesGrabadas(self):
		self.pararGrabacion()
		print self.ordenesGrabadas
		print self.enGrabacion
		for orden in self.ordenesGrabadas:
			self.tiempo.set(orden[1])
			self.actuar(orden[0])
	
	
	
				
root=Tk()
root.title ('maplinRobot Arm')
app=App(root)
root.mainloop()







	





