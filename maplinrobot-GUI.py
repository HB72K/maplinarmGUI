#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from ttk import *
import random
import pickle 

from comunicacion_con_brazo import comunicacion

class App:
	
	def __init__(self, master):
		"""iniciando la comunicacion con el brazo"""
		self.com=comunicacion()
		
		# ---------------------- Variables -------------------------
		self.master = master
		self.tiempo = DoubleVar()
		self.ordenesGrabadas=[]		#Ejemplo: ordenesGrabadas=[("base-izquierda", 1), ("base-derecha",1)]
		self.enGrabacion=BooleanVar()
		self.duration=1.0 # Duration (In seconds) for each action. Defaults to 1 second
		#---------------Ambiente Grafico- -----------#
		self.mainframe = Frame(self.master, padding = '3 3 12 12')
		self.makeWidgets()
		
	
	def makeWidgets(self):
		
		#hace que el marco se empaquete en el espacio disponible
	
		self.mainframe.grid(column=0, row= 0, sticky=(N,W,E,S))
		self.mainframe.columnconfigure(0, weight=1)
		self.mainframe.rowconfigure(0, weight=1)
		
		#pinza
		Label(self.mainframe, text='Pinza').grid(column=0, row=0, sticky=W)
		Button(self.mainframe, text="Abrir", command = lambda : self.actuar('abrir-pinza')).grid(column=1, row=0, sticky=W)
		Button(self.mainframe, text="Cerrar", command = lambda : self.actuar('cerrar-pinza')).grid(column=1, row=1, sticky=W)
		
		#separador verticales
		Label(self.mainframe, text='     ').grid(column=2, row=1, sticky=W)
		
		#base
		Label(self.mainframe, text='Base').grid(column=3, row=0, sticky=E)
		Button(self.mainframe, text="derecha", command = lambda : self.actuar('base-derecha') ).grid(column=4, row=0, sticky=W)
		Button(self.mainframe, text="izquierda", command = lambda : self.actuar('base-izquierda')).grid(column=4, row=1, sticky=W)
		
		#separador vertical
		Label(self.mainframe, text='     ').grid(column=5, row=1, sticky=W)
	
		#hombro
		Label(self.mainframe, text='Hombro').grid(column=6, row=0, sticky=E)
		Button(self.mainframe, text="subir", command = lambda : self.actuar('subir-hombro')).grid(column=7, row=0, sticky=W)
		Button(self.mainframe, text="bajar", command = lambda : self.actuar('bajar-hombro')).grid(column=7, row=1, sticky=W)
		
		#codo
		Label(self.mainframe, text='Codo').grid(column=0, row=4, sticky=W)
		Button(self.mainframe, text="subir", command = lambda : self.actuar('subir-codo')).grid(column=1, row=4, sticky=W)
		Button(self.mainframe, text="bajar", command = lambda : self.actuar('bajar-codo')).grid(column=1, row=5, sticky=W)
		
		#munneca
		Label(self.mainframe, text='Munneca').grid(column=3, row=4, sticky=W)
		Button(self.mainframe, text="subir", command = lambda : self.actuar('subir-munneca')).grid(column=4, row=4, sticky=W)
		Button(self.mainframe, text="bajar", command = lambda : self.actuar('bajar-munneca')).grid(column=4, row=5, sticky=W)
		
		#separador horizontal
		Label(self.mainframe, text=' ').grid(column=3, row=3, sticky=W)
		
		#luz
		Label(self.mainframe, text='Luz').grid(column=6, row=4, sticky=E)
		Button(self.mainframe, text="encender", command = lambda : self.actuar('encender-luz')).grid(column=7, row=4, sticky=W)
		Button(self.mainframe, text="apagar", command = lambda : self.actuar('apagar-luz')).grid(column=7, row=5, sticky=W)
		
		#grabacion
		Label(self.mainframe, text='Grabacion').grid(column=0, row=8, sticky=W)
		Button(self.mainframe, text="Ejecutar Grabacion", command = self.ejecutarOrdenesGrabadas).grid(column=0, row=9, sticky=W)
		Button(self.mainframe, text="Parar de Grabar", command = self.pararGrabacion).grid(column=0, row=10, sticky=W)
		Button(self.mainframe, text="Grabar", command = self.iniciarGrabacion).grid(column=1, row=9, sticky=W)
		Button(self.mainframe, text="Guardar", command = self.guardarGrabacion).grid(column=2, row=9, sticky=W)
		Button(self.mainframe, text="Cargar", command = self.cargarGrabacion).grid(column=3, row=9, sticky=W)
		Button(self.mainframe, text="Borrar", command = self.borrarOrdenesGrabadas).grid(column=4, row=9, sticky=W)
		
		Label(self.mainframe, text='Estado Grabacion ').grid(column=0, row=11, sticky=W)
		Label(self.mainframe, textvariable=self.enGrabacion).grid(column=0, row=12, sticky=W)
	
		
		#ordenes
		Label(self.mainframe, text='ordenes grabadas').grid(column=7, row=7, sticky=W)
		list = Listbox(self.mainframe, relief=SUNKEN)
		list.grid(row=8,column=7, sticky=E)	
		#list.config(selectmode=SINGLE, setgrid=1)
		self.listaOrdenes = list
		list.bind('<Double-1>', self.borrarOrden)
		
		
		
		#separador horizontal
		Label(self.mainframe, text='    ').grid(column=0, row=5, sticky=W)
		
		#tiempo deslizable
		Label(self.mainframe, text='Tiempo').grid(column=0, row=6, sticky=W)
		scale=Scale(self.mainframe, from_=1, to=4, orient=HORIZONTAL,
			command=self.onScale).grid(column=0, row=7)
		Label(self.mainframe, textvariable=self.tiempo,
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
			self.actualizarOrdenesGrabadas(comando,self.tiempo.get())
			
	
	# -----------------------------------------------------------	
	# Proceso de grabacion de ordenes y ejecucion de las mismas
	# -----------------------------------------------------------
	
	def iniciarGrabacion(self):
		self.enGrabacion.set(True)
		
	def pararGrabacion(self):
		self.enGrabacion.set(False)
	
	def actualizarOrdenesGrabadas(self,comando, tiempo):
		self.ordenesGrabadas.append((comando, tiempo))
		self.listaOrdenes.insert(END, comando + " " + str(int(tiempo)) + " seg")
		#print self.ordenesGrabadas
	
	def ejecutarOrdenesGrabadas(self):
		self.pararGrabacion()
		print self.ordenesGrabadas
		print self.enGrabacion
		for orden in self.ordenesGrabadas:
			self.tiempo.set(orden[1])
			self.actuar(orden[0])
			
	def guardarGrabacion(self):
		archivo = asksaveasfilename()		
		try:
			with open(archivo, 'wb') as mysavedata:
				pickle.dump(self.ordenesGrabadas, mysavedata)
		except IOError as err:
			print('File error: ' + str(err))
		except pickle.PickleError as perr:
			print('Pickling error: ' + str(perr))
		
	def cargarGrabacion(self):
		archivo = askopenfilename()
		try:
			with open(archivo, 'rb') as mysavedata:
				ordenes = pickle.load(mysavedata)
		except IOError as err:
			print('File error: ' + str(err))
		except pickle.PickleError as perr:
			print('Pickling error: ' + str(perr))
		finally:
			self.borrarOrdenesGrabadas()
			for comando in ordenes:
				self.actualizarOrdenesGrabadas(comando[0],comando[1])
			self.tiempo.set(ordenes[0][1])
			
	def borrarOrdenesGrabadas(self):
		self.ordenesGrabadas = []
		self.listaOrdenes.delete(0, self.listaOrdenes.size())
		
		
	def borrarOrden(self,event):
		indice = int(self.listaOrdenes.curselection()[0])
		print indice
		self.listaOrdenes.delete(indice) 
		del(self.ordenesGrabadas[indice])
		
	
				
root=Tk()
root.title ('maplinRobot Arm')
app=App(root)
root.mainloop()







	





