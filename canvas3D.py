#         _\|/_
#         (O-O)
# -----oOO-(_)-OOo----------------------------------------------------

#######################################################################
# ******************************************************************* #
# *             ROBOT Virtual  v3.0     23/06/2014 00:27            * #
# *      Funciona giro, subir y bajar, coger y soltar objetos       * #
# *                                                                 * #
# *         Elementos creados a partir de la clase 'Hueso'          * #
# *                                                                 * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################

# Importa las funcionalidades matematicas y en entorno gráfico Tkinter

from math import *
from Tkinter import *
from acciones import Acciones

# ******************************************************************* #
# *                 definicion de algunas constantes                * #
# ******************************************************************* #

ancho_canvas = 750  # Ancho del area de dibujo
alto_canvas = 500   # Altop del area de dibujo
xpantalla = 500     # offset eje X para situar el origen de coordenadas
ypantalla = 250     # offset eje Y para situar el origen de coordenadas
longitud_ejex = 210 # longitud del eje X
longitud_ejey = 180 # logitud del eje Y

frontalx,frontaly = 80,100  # offset ejes X,Y para situar la Mini Vista Frontal
cenitalx,cenitaly = 260,100 # offset ejes X,Y para situar la Mini Vista Cenital
escala_miniatura = .5       # reduccion para representar las vista sminiatura (0.4 y 0.5 como valores optimos)

angulo_paso_de_giro = pi/36  # paso giro para las rotaciones globales del brazo 
angulo_subida_bajada = pi/36 # paso de giro para los movimientos verticales
angulo_total = 0

mano_cerrada = 0
mano_ocupada = 0
cierre = 0


def crear_robot():
    global robot, dummy, pinza, objetos
    hueso_1 = Hueso (nodo_1.punto, nodo_2.punto, 'blue',6)
    hueso_2 = Hueso (nodo_2.punto, nodo_3.punto, 'yellow', 6)
    hueso_3 = Hueso (nodo_3.punto, nodo_4.punto, 'DeepPink', 6) 
    hueso_4 = Hueso (nodo_5.punto, nodo_6.punto, 'DeepPink', 6)
    hueso_5 = Hueso (nodo_5.punto, nodo_7.punto, 'DeepPink', 8)
    hueso_6 = Hueso (nodo_6.punto, nodo_8.punto, 'DeepPink', 8)
    robot = [hueso_1, hueso_2, hueso_3, hueso_4]
    pinza = [hueso_5, hueso_6]

## robot fantasma (activar visualización solo para pruebas)
    hues_1 = Hueso (nodo_1.punto_ref, nodo_2.punto_ref, 'yellow', 3,(1,1))
    hues_2 = Hueso (nodo_2.punto_ref, nodo_3.punto_ref, 'yellow', 3,(1,1))
    hues_3 = Hueso (nodo_3.punto_ref, nodo_4.punto_ref, 'yellow', 3,(1,1))
    hues_4 = Hueso (nodo_5.punto_ref, nodo_6.punto_ref, 'yellow', 3,(1,1))
    hues_5 = Hueso (nodo_5.punto_ref, nodo_7.punto_ref, 'yellow', 3,(1,1))
    hues_6 = Hueso (nodo_6.punto_ref, nodo_8.punto_ref, 'yellow', 3,(1,1))
    dummy = []# hues_1, hues_2, hues_3, hues_4, hues_5, hues_6


    ## lista de objetos que se creó mediante la Class 'Ladrillo'
    ## De esta forma regeneramos los objetos con sus cambios.
    objetos = ladrillo_1.bloque + ladrillo_2.bloque + ladrillo_3.bloque 

    return (robot, dummy, objetos)


# función para borrar la pantalla
def borrar_y_dibujar_ejes ():
    '''Borra completamente el area de dibujo y redibuja
    los ejes de coordenadas y etiquetas de los ejes'''
    canvas.delete("all")
    canvas.create_line(xpantalla-longitud_ejex, ypantalla,xpantalla+longitud_ejex, ypantalla, width=1, fill = 'SlateGray', dash = (3, 10)) #  Eje horizontal desde x1,y1 hasta x2,y2
    canvas.create_line(xpantalla, ypantalla-longitud_ejey, xpantalla, ypantalla+longitud_ejey, width=1, fill = 'SlateGray', dash=(3, 10)) #  Eje vertical.....
    canvas.create_line(xpantalla-longitud_ejex/2, ypantalla+longitud_ejex/2,xpantalla+longitud_ejex/2,  ypantalla- longitud_ejex/2, width=1, fill = 'SlateGray', dash=(1, 10, 1, 1))

    canvas.create_text(xpantalla-longitud_ejex, ypantalla-10, text="180º", fill='Black',
                    activefill='White', font=('verdana', 8,'bold','italic'))
    canvas.create_text(xpantalla-longitud_ejex/2, ypantalla+longitud_ejex/2, text="90º", fill='Black',
                    activefill='White', font=('verdana', 8,'bold','italic'))
    canvas.create_text(xpantalla+longitud_ejex, ypantalla-10, text="0º", fill='Black',
                    activefill='White', font=('verdana', 8,'bold','italic'))
    canvas.create_text(xpantalla+longitud_ejex/2, ypantalla-longitud_ejex/2, text="270º", fill='Black',
                    activefill='White', font = ('verdana', 8,'bold','italic'))
    canvas.create_text(xpantalla+longitud_ejex, ypantalla+10, text = "Eje X", fill = 'Gray', font = ('verdana', 9,'bold'))
    canvas.create_text(xpantalla-longitud_ejex/2+40, ypantalla+longitud_ejex/2, text = "Eje Z", fill = 'Gray', font = ('verdana', 9,'bold'))
    canvas.create_text(xpantalla, ypantalla-longitud_ejey-20, text ="Eje Y", fill = 'Gray', font = ('verdana', 9,'bold'))



#  Etiquetas indicando el nombre de las Rotulas
def Etiquetar_Robot():
     i = 0
     while i < 3:
          texto = "T " + str (i)
          canvas.create_text(robot[i].inicio2D[0]+xpantalla, ypantalla-robot[i].inicio2D[1],
                             text = texto, fill = 'Black',activefill = 'Yellow',
                             font = ('verdana', 10, 'bold', 'italic'))
          i = i + 1
     canvas.create_text (robot[i].inicio2D[0]+xpantalla+10, ypantalla -15 -robot[i].inicio2D[1], text = "MANO", fill = 'Black', activefill = 'Yellow',
                        font = ('verdana', 7))
     return ()

def control_de_objetos():
    global mano_ocupada, cierre
 
    objeto_a_mano = 0
    for ladrillo in ladrillos:
        if abs((ladrillo.centro[0] - nodo_4.punto[0])) < 15 and abs((ladrillo.centro[1] - nodo_4.punto[1])) < 15 and abs((ladrillo.centro[2] - nodo_4.punto[2])) < 15:
            objeto_a_mano = 1
            ladrillo.color = 'deep sky blue'
        else:
            ladrillo.color = ladrillo.color_original
            objeto_a_mano = 0  

        if mano_cerrada == 1 and objeto_a_mano == 1 and ladrillo.agarrado == 0 and mano_ocupada == 0 and cierre == 1:
            ladrillo.color = 'yellow'
            ladrillo.agarrado = 1
            mano_ocupada = 1
            
        # ****  Los ladrillos se apilan  ****
        if mano_cerrada == -1 and ladrillo.agarrado == 1:
            suelo = 0
            x = ladrillo.centro[0]
            z = ladrillo.centro[2]
            for obstaculo in ladrillos:
                if obstaculo != ladrillo and abs((obstaculo.centro[0] - x)) < 15  and abs((obstaculo.centro[2] - z)) < 15:
                    suelo += obstaculo.alto                   
            ladrillo.color = ladrillo.color_original
            ladrillo.centro = (nodo_4.punto[0],suelo,nodo_4.punto[2])
            ladrillo.agarrado = 0
            mano_ocupada = 0

##        # ****  Los ladrillos caen al suelo  ****
##        if mano_cerrada == -1 and ladrillo.agarrado == 1:
##            ladrillo.color = ladrillo.color_original
##            ladrillo.centro = (nodo_4.punto[0],0,nodo_4.punto[2])
##            ladrillo.agarrado = 0
##            mano_ocupada = 0
            
        if ladrillo.agarrado == 1:
            ladrillo.centro = nodo_4.punto
            ladrillo.color = 'yellow'
            
        ladrillo.solido()

    cierre = 0
    return()

def regenerar_pantalla():
    # Borrar la pantalla y redibujar los ejes de coordenadas
    borrar_y_dibujar_ejes ()
    robot, dummy, objetos = crear_robot()

    # Dibujar el brazo robot en su posicion inicial
    for hueso in robot:
        hueso.dibujar()
        hueso.dibujar_cenital(cenitalx,cenitaly) # coodenadas X,Y absolutas, de la posicion del centro del widget en el canvas
        hueso.dibujar_frontal(frontalx,frontaly) # coodenadas X,Y absolutas, de la posicion del centro del widget en el canvas
        hueso.sombra()
    for fantasma in dummy:
        fantasma.dibujar()
        fantasma.sombra()
    for dedo in pinza:
        dedo.dibujar()
        dedo.dibujar_cenital(cenitalx,cenitaly)
        dedo.dibujar_frontal(frontalx,frontaly)
        dedo.sombra()
    for arista in objetos:
        arista.dibujar()
        arista.dibujar_cenital(cenitalx,cenitaly)
        arista.dibujar_frontal(frontalx,frontaly)
    for ladrillo in ladrillos:
        if ladrillo.agarrado == 1:
            ladrillo.sombra_ladrillo()
        
    Etiquetar_Robot()




# Aplicar un giros en el eje Y -  LLEGAMOS DESDE EL BOTON
def Girar_Base(sentido):
    global angulo_total
    angulo_total = angulo_total + sentido * angulo_paso_de_giro
    for articulacion in articulaciones:
        articulacion.girar(nodo_1.punto,sentido)
    control_de_objetos()
              
    # Llamamos ala funcion que borra la pantalla y redibuja los elementos
    regenerar_pantalla()

    # Formateo y visualizacion de algunas variables en el Display
    grados = degrees (angulo_total)
    if grados >= 360 :
        grados = grados - 360
    if grados < 0 :
        grados = grados + 360

    entrada_0000.set(round(angulo_total, 4))
    entrada_0001.set(round(grados))
    entrada_0002.set("BASE   ")
    entrada_0003.set("Girando")



# Aplicar elevaciones y bajadas del brazo - LLEGAMOS DESDE EL BOTON
def subir_bajar_brazo(bisagra, sentido):

    for indice in range(0,len(articulaciones)):
        if(articulaciones[indice].punto_ref == bisagra):
            i = indice +1  # determinar que 'huesos' se mueven y cuales no
            display = indice # esto es para el caso de que se visualice datos
    while i < len(articulaciones):
        articulaciones[i].subir_bajar(bisagra, sentido)
        i = i + 1
    control_de_objetos()

    # Llamamos a la funcion que borra la pantalla y redibuja los elementos
    regenerar_pantalla()

    # formateo y visualizacion de algunas variables en el Display
    direccion = sentido
    if display == 0:
        direccion = direccion*(-1)
    if direccion < 0:
        mover = 'BAJANDO'
    if direccion > 0:
        mover = 'SUBIENDO'


    grados = degrees(angulo_total)
    grados = (int(grados*10)/10) + .11
    grados = round(grados,0)
    if grados >= 360:
        grados = grados - 360
    if grados < 0:
        grados = grados + 360

    entrada_0000.set(round(angulo_total,4))
    entrada_0001.set(round(grados))
    entrada_0002.set(display)
    entrada_0003.set(mover)

    
# Juntar y separar los dedos de la pinza    
def Pinza(fuerza):
    global mano_cerrada
    global cierre
    i = len(articulaciones)-4

    if articulaciones[i].punto_ref[2] == 0 and fuerza > 0:
        fuerza = 0
        mano_cerrada = 1
        cierre = 1
    if articulaciones[i].punto_ref[2] == -12 and fuerza < 0:
        fuerza = 0
        mano_cerrada = -1

    articulaciones[i].punto_ref = (articulaciones[i].punto_ref[0],articulaciones[i].punto_ref[1],
                                   articulaciones[i].punto_ref[2] + fuerza)
    articulaciones[i+2].punto_ref = (articulaciones[i+2].punto_ref[0],articulaciones[i+2].punto_ref[1],
                                   articulaciones[i+2].punto_ref[2] + fuerza)

    articulaciones[i+1].punto_ref = (articulaciones[i+1].punto_ref[0],articulaciones[i+1].punto_ref[1],
                                   articulaciones[i+1].punto_ref[2] - fuerza)
    articulaciones[i+3].punto_ref = (articulaciones[i+3].punto_ref[0],articulaciones[i+3].punto_ref[1],
                                   articulaciones[i+3].punto_ref[2] - fuerza)
    for articulacion in articulaciones:
        articulacion.subir_bajar (nodo_1.punto_ref, 0)# simulamos un giro 0º para que se actualice
    control_de_objetos()

    regenerar_pantalla()


## ------------------------------------------------------------------------------------
##  DEFINICION DE LA CLASE << HUESO >>
##  a la que pertenecen los segmentos que forman el robot y los objetos    
## ------------------------------------------------------------------------------------

class Hueso:
    '''Definicion de las caracteristicas basicas iniciales del hueso'''
    
    def __init__ (self,inicio,extremo,color,grosor, opacidad =()):

        self.inicio = inicio
        self.extremo = extremo
        self.inicio2D = self.calcular_coordenadas_2D(self.inicio)
        self.extremo2D = self.calcular_coordenadas_2D(self.extremo)
        self.inicio_sombra = self.calcular_coordenadas_2D((self.inicio[0],0,self.inicio[2]))
        self.extremo_sombra = self.calcular_coordenadas_2D((self.extremo[0],0,self.extremo[2]))
        self.color = color
        self.grosor = grosor
        self.opacidad = opacidad
        

    ## ------------------------------------------------------------------------------------
    ##  Funciones de transformacion de la clase HUESO      
    ## ------------------------------------------------------------------------------------
    def calcular_coordenadas_2D(self, punto3d):
        '''toma puntos del espacio 3D y calcula sus proyeccion 2D para su correcta
        representacion sobre la pantalla'''
        x = punto3d[0]
        y = punto3d[1]
        z = punto3d[2]
        x2d = x - z * 0.375 # ajuste de proporcion del eje Z
        y2d = y - z * 0.375 # ajuste de proporcion del eje Z
        punto2d = (x2d, y2d)
        return (punto2d)
    
    ## ------------------------------------------------------------------------------------
    ##   Metodos a llamar para la clase HUESO
    ## ------------------------------------------------------------------------------------

    # Dibujar los huesos que conforman el brazo
    def dibujar_cenital(self, x, y):
        '''Crea las vista cenital miniatura'''
        canvas.create_line(x-80, y, x+80, y, width=1, fill = 'SlateGray', dash = (3, 10)) #  Eje horizontal desde x1,y1 hasta x2,y2
        canvas.create_line(x, y-80, x, y+80, width=1, fill = 'SlateGray', dash=(3, 10)) #  Eje vertical.....

        canvas.create_line((self.inicio[0]* escala_miniatura + x), (y + self.inicio[2]* escala_miniatura),
                           (self.extremo[0]*escala_miniatura + x), (y + self.extremo[2]* escala_miniatura),
                            width = 2, fill = self.color, dash = self.opacidad,
                            capstyle = ROUND, joinstyle = ROUND)
    
    def dibujar_frontal(self, x, y):
        '''Crea las vista frontal miniatura'''
        canvas.create_line(x-80, y, x+80, y, width=1, fill = 'SlateGray', dash = (3, 10)) #  Eje horizontal desde x1,y1 hasta x2,y2
        canvas.create_line(x, y-80, x, y+80, width=1, fill = 'SlateGray', dash=(3, 10)) #  Eje vertical.....
        
        canvas.create_line((self.inicio[0]* escala_miniatura + x), (y - self.inicio[1]* escala_miniatura),
                           (self.extremo[0]* escala_miniatura + x), (y - self.extremo[1]* escala_miniatura),
                            width = 2, fill = self.color, dash = self.opacidad,
                            capstyle = ROUND, joinstyle = ROUND)

    def dibujar(self):
        '''Crea las lineas que definen a cada hueso'''
        canvas.create_line((self.inicio2D[0] + xpantalla), (ypantalla - self.inicio2D[1]),
                           (self.extremo2D[0] + xpantalla), (ypantalla - self.extremo2D[1]),
                            width = self.grosor, fill = self.color, dash = self.opacidad,
                            capstyle = ROUND, joinstyle = ROUND)

    def sombra(self):
        '''Crea las lineas que definen las sombras'''
        canvas.create_line((self.inicio_sombra[0] + xpantalla), (ypantalla - self.inicio_sombra[1]),
                           (self.extremo_sombra[0] + xpantalla), (ypantalla - self.extremo_sombra[1]),
                            width = 7, fill = 'Dim Gray', stipple='gray25',
                            capstyle = ROUND, joinstyle = ROUND)




## ------------------------------------------------------------------------------------
##  DEFINICION DE LA CLASE << NODO >>
##  a la que pertenecen las rotulas que forman los huesos y que sirven para girarlos    
## ------------------------------------------------------------------------------------


class Nodo:
    '''Definicion de las caracteristicas basicas iniciales del Nodo'''
   
    def __init__ (self,punto):
        
        self.punto = punto # Almacena las coordenadas 3D de los nodos
        self.punto_ref = punto # Copia del nodo para las transformaciones verticales

    ## ------------------------------------------------------------------------------------
    ##  Funciones de transformacion de la clase NODO     
    ## ------------------------------------------------------------------------------------

    def girar_vertices (self, horizontal, vertical , centro_h, centro_v , angulo):
        '''calculos trigonometricos para el calculo de las transformaciones'''
        xa = horizontal - centro_h
        ya = vertical - centro_v
        modulo =(xa**2 + ya**2)**0.5
        angulo_inicial = atan2(ya, xa)
        angulo_final = angulo_inicial + angulo
        horizontal_con_giro = modulo * cos (angulo_final) + centro_h
        vertical_con_giro = modulo * sin (angulo_final) + centro_v
        return (horizontal_con_giro, vertical_con_giro)

    
    ## ------------------------------------------------------------------------------------
    ##    Metodos a llamar para la clase NODO
    ## ------------------------------------------------------------------------------------

    # Calcular la rotacion en el eje Y de los huesos que conforman el brazo
    # el 'sentido' de giro toma valores +1 o -1
    
    def girar(self, rotula, sentido):
        '''llamada a la funcion de calculos trigonometricos con los
        parametros apra realizar un giro respecto al eje Y'''
        
        x, z = self.girar_vertices(self.punto[0], self.punto[2],
                                         nodo_1.punto[0],nodo_1.punto[1], sentido*angulo_paso_de_giro)
        self.punto=(x, self.punto[1], z)

 
    def subir_bajar(self, rotula, sentido):
        '''llamada a la funcion de calculos trigonometricos con los
        parametros para realizar un giro verticales de las rotulas. Se
        utilizan apra ello la propiedad la copia de los puntos que se
        mantiene siempre en el plano XY'''

        x, y = self.girar_vertices(self.punto_ref[0], self.punto_ref[1], 
                                             rotula[0],rotula[1], sentido*angulo_subida_bajada)
        # nodos de referencia una vez movido verticalmente
        self.punto_ref = (x, y, self.punto_ref[2])
        # Devuelve los nodos a su plano vertical original
        x, z = self.girar_vertices(self.punto_ref[0], self.punto_ref[2],
                                         nodo_1.punto[0],nodo_1.punto[2], angulo_total)
        # Actualiza el punto con los valores de _ref devueltos al plano
        self.punto=(x, self.punto_ref[1], z)

        


## ------------------------------------------------------------------------------------
##  DEFINICION DE LA CLASE << LADRILLO >>
##  a la que pertenecen los objetos . Se apolla en la clase HUESO   
## ------------------------------------------------------------------------------------

class Ladrillo:
    '''Utilizada para crear los objetos sobre el escenario. Toma un
    punto inicial y llama a la clse Hueso depetidas veces hasta formar un prisma'''

    def __init__ (self, centro, ancho, alto, color='blue', grosor = 3):

        self.centro = centro
        self.vertice = (self.centro[0]-(ancho/2),self.centro[1],self.centro[2]-(ancho/2))
        self.ancho = ancho
        self.alto = alto
        self.color_original = color
        self.color = color
        self.grosor = grosor
        self.agarrado = 0

    def solido(self):
        '''metodo que genera el prisma completo a partir de el centro del
        objeto y sus propiedades basicas: color, grosor de linea, ancho y alto '''
        self.vertice = (self.centro[0]-(self.ancho/2),self.centro[1], self.centro[2]-(self.ancho/2))
        
        self.arista_1 = Hueso (self.vertice, (self.vertice[0],self.vertice[1],self.vertice[2]+self.ancho),
                               self.color, self.grosor)
        self.arista_2 = Hueso (self.arista_1.extremo,
                               (self.arista_1.extremo[0]+self.ancho,self.vertice[1],self.arista_1.extremo[2]),
                               self.color, self.grosor)
        self.arista_3 = Hueso (self.arista_2.extremo,
                               (self.arista_1.inicio[0]+self.ancho,self.vertice[1],self.arista_1.inicio[2]),
                               self.color, self.grosor)
        self.arista_4 = Hueso (self.arista_3.extremo, self.arista_1.inicio, self.color, self.grosor)

        self.arista_5 = Hueso ((self.arista_1.inicio[0],self.vertice[1]+self.alto,self.arista_1.inicio[2]),
                               (self.arista_1.extremo[0],self.vertice[1]+self.alto,self.arista_1.extremo[2]),
                                self.color, self.grosor)
        self.arista_6 = Hueso (self.arista_5.extremo,
                               (self.arista_5.extremo[0]+self.ancho,self.vertice[1]+self.alto,self.arista_5.extremo[2]),
                               self.color, self.grosor)
        self.arista_7 = Hueso (self.arista_6.extremo,
                               (self.arista_5.inicio[0]+self.ancho,self.vertice[1]+self.alto, self.arista_5.inicio[2]),
                                self.color, self.grosor)
        self.arista_8 = Hueso (self.arista_7.extremo, self.arista_5.inicio, self.color, self.grosor)
        self.arista_9 = Hueso (self.arista_1.extremo, self.arista_5.extremo, self.color,self.grosor)
        self.arista_10 = Hueso (self.arista_2.extremo, self.arista_6.extremo, self.color, self.grosor)
        self.arista_11 = Hueso (self.arista_3.extremo, self.arista_7.extremo, self.color, self.grosor)
        self.arista_12 = Hueso (self.arista_4.extremo, self.arista_8.extremo, self.color, self.grosor)
            
            
        self.bloque = [self.arista_2, self.arista_3, self.arista_5, self.arista_6, self.arista_7,
                   self.arista_8, self.arista_9, self.arista_10, self.arista_11]


    def sombra_ladrillo(self):
        ''' Cremos las sombras de los objetos si estan elevados del suelo '''
        
        canvas.create_polygon(self.arista_1.inicio_sombra[0] + xpantalla,
                              ypantalla - self.arista_1.inicio_sombra[1],
                              self.arista_2.inicio_sombra[0] + xpantalla,
                              ypantalla - self.arista_2.inicio_sombra[1],
                              self.arista_3.inicio_sombra[0] + xpantalla,
                              ypantalla - self.arista_3.inicio_sombra[1],
                              self.arista_4.inicio_sombra[0] + xpantalla,
                              ypantalla - self.arista_4.inicio_sombra[1],
                              fill='slate blue', stipple='gray50')





# ******************************************************************* #
# *                       INICIO DEL PROGRAMA                       * #
# ******************************************************************* #


# Definicion de los elementos del brazo, mediante el punto de inicio, el punto final, color y grosor de linea

nodo_1 = Nodo ((0,0,0))
nodo_2 = Nodo ((-70,70,0))
nodo_3 = Nodo ((0,140,0))
nodo_4 = Nodo ((50,140,0))
nodo_5 = Nodo ((50,140,-12))
nodo_6 = Nodo ((50,140,12))
nodo_7 = Nodo ((65,140,-12))
nodo_8 = Nodo ((62,140,12))


  
# Creacion del robot agrupando sus huesos
articulaciones = [nodo_1, nodo_2, nodo_3, nodo_4, nodo_5, nodo_6, nodo_7, nodo_8] #]

# Creacion de objetos mediante la Class 'Ladrillo' (la primera vez)
ladrillo_1 = Ladrillo ((130,0,0), 20, 20, 'blue2', 3)
ladrillo_1.solido()

ladrillo_2 = Ladrillo ((-100,0,90), 20, 20, 'green4', 3)
ladrillo_2.solido()

ladrillo_3 = Ladrillo ((90,0,150), 20, 20, 'tomato', 3)
ladrillo_3.solido()

# La variable ladrillos es una lista de los 'objetos' completos.
ladrillos =[ladrillo_1,ladrillo_2,ladrillo_3]
# La variable objetos es una lista de las propiedades .bloque de los
# objetos, decir de las lineas que los componen y que sirven apra
# dibujarlos
objetos = ladrillo_1.bloque + ladrillo_2.bloque + ladrillo_3.bloque 


# Conectando con el modulo acciones
accion = Acciones()




#######################################################################
#                                                                     #
#    Crear la ventana 'ROOT' y poner nombre en la barra de titulo     #
#    dibujar elementos iniciales, ejes, brazo, etiquetas...           #
#              Es decir, creacion del entorno grafico                 #
#                                                                     #


# Crear the root window y poner nombre en la barra de titulo
root = Tk()
root.title('SIMULADOR de Brazo Robot v3.0 r1 - Eulogio López Cayuela 2014')
# root.iconbitmap('minion02.ico')

# Tamaño y posición de la ventana principal
# pasados como parametros al constructor 'geometry'
w = 900
h = 600
px = 100
py = 10

# Ventana principal
# geometry(ancho * alto + desplazamientoX + desplazamientoY)
root.geometry("%dx%d+%d+%d" % (w, h, px, py))

# Creacion del area de dibujo
canvas = Canvas(root, width = ancho_canvas, height=alto_canvas)


# Llamamos ala funcion que borra la pantalla y redibuja los elementos
regenerar_pantalla()




##########################################################
#    DISEÑO DEL ASPECTO VISUAL DE ETIQUETAS Y BOTONES    #
##########################################################



# MARCO para envolver la zona de muestra de datos (DISPLAY)
marco01 = LabelFrame(root, text = "Datos de interés", bd = 1).place(width = 265, height = 80, x = 5, y = 480)

# ETIQUETAS para las CAJAS DE TEXTO
etiqueta00 = Label(root, text = "Radianes").place(width = 50, height = 30, x = 20, y = 495)
etiqueta01 = Label(root, text = "Grados").place(width = 50, height = 30, x = 80, y = 495)
etiqueta02 = Label(root, text = "Rotula").place(width = 50, height= 30, x = 140, y = 495)
etiqueta03 = Label(root, text = "Dirección").place(width = 50, height = 30, x = 200, y = 495)

# VARIABLES para la recoleccion de datos
entrada_0000 = StringVar()
entrada_0001 = StringVar()
entrada_0002 = StringVar()
entrada_0003 = StringVar()
entrada_0000.set(angulo_total)
entrada_0001.set("0")
entrada_0002.set(" --- ")
entrada_0003.set("Reposo")

# CAJAS DE TEXTO para la muestra de datos útiles
mostrar_Radianes = Entry(root,textvariable = entrada_0000, bg = 'green', fg = 'Yellow', justify = RIGHT,
                       font=('wst_engl', 10, 'bold')).place(width = 50, height = 20, x = 20, y = 520)
mostrar_Grados = Entry(root, textvariable = entrada_0001, bg = 'green',fg = 'Yellow', justify = RIGHT,
                     font=('wst_engl', 10, 'bold')).place(width = 50, height = 20, x = 80, y = 520)
mostrar_Rotula = Entry(root, textvariable=entrada_0002,bg='green',fg = 'Yellow', justify =RIGHT,
                     font=('wst_engl', 10, 'bold')).place(width=50, height=20, x = 140, y = 520)
mostrar_Movimiento = Entry(root, textvariable = entrada_0003, bg='green', fg = 'Yellow', justify = CENTER,
                         font=('Arial', 8, 'bold')).place(width = 55, height = 20, x = 200, y = 520)




# MARCO para envolver la zona de la botonera de control
marco02 = LabelFrame(root, text = "CONTROLES DEL BRAZO", bd = 2).place(width = 595, height = 110, x = 5, y = 580)


# BOTONES para asignar ordenes al Brazo Robot

# Aplicar Giros sobre la base
boton_1 = Button(root,text="Rotar Brazo (-)",
                 command= lambda: Girar_Base(-1) or accion.actuar('base-izquierda'))
boton_1.place(bordermode = INSIDE, width = 120, height = 30,  x = 20, y = 600)

boton_2 = Button(root,text = "Rotar Brazo (+)",
                 command = lambda: Girar_Base(1) or accion.actuar('base-derecha'))
boton_2.place(bordermode = INSIDE, width = 120, height = 30,  x = 20, y = 650)
# TRAMO 1 Subir y Bajar (llama a la funcion 'Subir_Bajar' con los parametros (sentido y rotula)
boton_3 = Button(root, text = "Subir T(1)",
                 command = lambda: subir_bajar_brazo(nodo_1.punto_ref, 1) or accion.actuar('subir-hombro'))
boton_3.place(bordermode = INSIDE, width = 90, height = 30,  x = 160, y = 600)

boton_4 = Button(root,text="Bajar T(1)",
                 command = lambda: subir_bajar_brazo(nodo_1.punto_ref, -1) or accion.actuar('bajar-hombro'))
boton_4.place(bordermode = INSIDE, width = 90, height = 30,  x = 160, y = 650)

# TRAMO 2 Subir y Bajar (llama a la funcion 'Subir_Bajar' con los parametros (sentido y rotula)
boton_5 = Button(root, text = "Subir T(2)",
                 command = lambda: subir_bajar_brazo(nodo_2.punto_ref, 1) or accion.actuar('subir-codo') )
boton_5.place(bordermode = INSIDE, width = 90, height = 30,  x = 270, y = 600)

boton_6 = Button(root, text = "Bajar T(2)",
                 command = lambda:subir_bajar_brazo(nodo_2.punto_ref, -1) or accion.actuar('bajar-codo') )
boton_6.place(bordermode = INSIDE, width = 90, height = 30,  x = 270, y = 650)

# TRAMO 3 Subir y Bajar (llama a la funcion 'Subir_Bajar' con los parametros (sentido y rotula)
boton_7 = Button(root, text = "Subir MANO",
                 command = lambda: subir_bajar_brazo(nodo_3.punto_ref, 1) or accion.actuar('subir-munneca'))
boton_7.place(bordermode = INSIDE, width = 90, height = 30,  x = 380, y = 600)

boton_8 = Button(root,text="Bajar MANO",
                 command = lambda: subir_bajar_brazo(nodo_3.punto_ref, -1) or accion.actuar('bajar-munneca'))
boton_8.place(bordermode = INSIDE, width = 90, height = 30,  x = 380, y = 650)

## PINZA Cierra y Abre la mano del Robot mediante la funcion 'Pinza' mediante el parametro (fuerza)
boton_9 = Button(root,text = "Abrir Pinza",
                 command = lambda: Pinza(-4) or accion.actuar('abrir-pinza'))
boton_9.place(bordermode = INSIDE, width = 90, height = 30,  x = 490, y = 600)

boton_10 = Button(root, text = "Cerrar Pinza",
                 command = lambda: Pinza(+4) or accion.actuar('cerrar-pinza'))
boton_10.place(bordermode = INSIDE, width = 90, height = 30,  x = 490, y = 650)

# SALIR, Boton para salir de la aplicación
boton_0 = Button(root, text = "SALIR",fg = "white", bg = "Blue", command=root.destroy)
boton_0.place(bordermode = INSIDE, width = 120, height = 30,  x= 1170, y = 650)


    
# Visualizar area de dibujo
canvas.pack()

# ******************************************************************* #
#              FIN de la creacion del entorno grafico                 #
# ******************************************************************* #

# Atender eventos
root.mainloop()

#######################################################################
#                                                                     #
#                           FIN DEL PROGRAMA                          #
#                                                                     #
#######################################################################


