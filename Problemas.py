

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from types import MethodType

def escribir_dama(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    x, y  = self.inv(atomo)
    return f"La dama{neg} está en la casilla ({x},{y})"

def escribir_rejilla(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    n, x, y  = self.inv(atomo)
    return f"El número {n}{neg} está en la casilla ({x},{y})"

class Caballos:

    '''
    Clase para representar el problema de poner
    tres caballos en un tablero de ajedrez sin que se
    puedan atacar el uno al otro.
    '''

    def __init__(self):
        self.DenC = Descriptor([8,8])
        self.DenC.escribir = MethodType(escribir_dama, self.DenC)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        self.reglas = [r1, r2, r3]


    def regla1(self):
        casillas = [(x,y) for x in range(8) for y in range(8)]
        lista = []
        for c in casillas:
            lista_y = list()
            for z in range(8):
                if(z != c.x):
                    lista_y.append('-' + DenC.P([z,y])) 
                
            formula = '(' + self.DenC.P([x,y]) + ">" + Ytoria(lista_y) + ')'
            lista.append(formula)
            
        return Yoria(lista)

    def regla2(self):
        
        casillas = [(x,y) for x in range(8) for y in range(8)]
        lista = []
        for c in casillas:
            lista_y = list()
            for z in range(8):
                if(z != c.y):
                    lista_y.append('-' + DenC.P([x,z])) 
                
            formula = '(' + self.DenC.P([x,y]) + ">" + Ytoria(lista_y) + ')'
            lista.append(formula)
            
        return Yoria(lista)

    def regla3(self):
        casillas = [(x,y) for x in range(8) for y in range(8)]
        combinaciones = list(combinations(casillas, 8))
        lista = []
        for c in casillas:
            lista_y = list()
            for z in range(8):
                for w in range(8):
                    if(abs((x-z)/(y-w)) == 1):
                        lista_y.append('-' + DenC.P([z,w]))
                
        formula = '(' + self.DenC.P([x,y]) + ">" + Ytoria(lista_y) + ')'
        lista.append(formula)
            
        return Yoria(lista)
    
    
    

    def visualizar(self, I):
        # Inicializo el plano que contiene la figura
        fig, axes = plt.subplots()
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        # Dibujo el tablero
        step = 1./3
        tangulos = []
        # Creo los cuadrados claros en el tablero
        tangulos.append(patches.Rectangle(\
                                        (0, step), \
                                        step, \
                                        step,\
                                        facecolor='cornsilk')\
                                        )
        tangulos.append(patches.Rectangle(*[(step, 0), step, step],\
                facecolor='cornsilk'))
        tangulos.append(patches.Rectangle(*[(2 * step, step), step, step],\
                facecolor='cornsilk'))
        tangulos.append(patches.Rectangle(*[(step, 2 * step), step, step],\
                facecolor='cornsilk'))
        # Creo los cuadrados oscuros en el tablero
        tangulos.append(patches.Rectangle(*[(2 * step, 2 * step), step, step],\
                facecolor='lightslategrey'))
        tangulos.append(patches.Rectangle(*[(0, 2 * step), step, step],\
                facecolor='lightslategrey'))
        tangulos.append(patches.Rectangle(*[(2 * step, 0), step, step],\
                facecolor='lightslategrey'))
        tangulos.append(patches.Rectangle(*[(step, step), step, step],\
                facecolor='lightslategrey'))
        tangulos.append(patches.Rectangle(*[(0, 0), step, step],\
                facecolor='lightslategrey'))
        # Creo las líneas del tablero
        for j in range(3):
            locacion = j * step
            # Crea linea horizontal en el rectangulo
            tangulos.append(patches.Rectangle(*[(0, step + locacion), 1, 0.005],\
                    facecolor='black'))
            # Crea linea vertical en el rectangulo
            tangulos.append(patches.Rectangle(*[(step + locacion, 0), 0.005, 1],\
                    facecolor='black'))
        for t in tangulos:
            axes.add_patch(t)
        # Cargando imagen de caballo
        arr_img = plt.imread("./img/caballo.png", format='png')
        imagebox = OffsetImage(arr_img, zoom=0.1)
        imagebox.image.axes = axes
        # Creando las direcciones en la imagen de acuerdo a literal
        direcciones = {}
        direcciones[(0,2)] = [0.165, 0.835]
        direcciones[(1,2)] = [0.5, 0.835]
        direcciones[(2,2)] = [0.835, 0.835]
        direcciones[(0,1)] = [0.165, 0.5]
        direcciones[(1,1)] = [0.5, 0.5]
        direcciones[(2,1)] = [0.835, 0.5]
        direcciones[(0,0)] = [0.165, 0.165]
        direcciones[(1,0)] = [0.5, 0.165]
        direcciones[(2,0)] = [0.835, 0.165]
        for l in I:
            if I[l]:
                x, y = self.CenC.inv(l)
                ab = AnnotationBbox(imagebox, direcciones[(x,y)], frameon=False)
                axes.add_artist(ab)
        plt.show()
