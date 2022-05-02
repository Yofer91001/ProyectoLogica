from clases import *
from declarations import *
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

class Damas:

    '''
    Clase para representar el problema de poner
    ocho damas en un tablero de ajedrez sin que se
    puedan atacar la una a la otra.
    '''

    def __init__(self):
        self.DenC = Descriptor([8,8])
        self.DenC.escribir = MethodType(escribir_dama, self.DenC)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        self.reglas = [r1, r2, r3]


    def regla1(self):
        
        lista = []
        for c in casillas:
            lista_y = list()
            for z in range(8):
                if(z != c[0]):
                    lista_y.append('-' + self.DenC.P([z,c[1]] ) ) 
                
            formula = '(' + self.DenC.P([c[0],c[1]]) + ">" + Ytoria(lista_y) + ')'
            lista.append(formula)
            
        return Ytoria(lista)

    def regla2(self):
        
        
        lista = []
        for c in casillas:
            lista_y = list()
            for z in range(8):
                if(z != c[1]):
                    lista_y.append('-' + self.DenC.P([c[0],z])) 
                
            formula = '(' + self.DenC.P([c[0],c[1]]) + ">" + Ytoria(lista_y) + ')'
            lista.append(formula)
            
        return Ytoria(lista)

    def regla3(self):
        
        combinaciones = list(combinations(casillas, 8))
        lista = []
        for c in casillas:
            lista_y = list()
            for z in range(8):
                for w in range(8):
                    if(abs((c[0]-z)/(c[1]-w)) == 1):
                        lista_y.append('-' + self.DenC.P([z,w]))
                
        formula = '(' + self.DenC.P([c[0],c[1]]) + ">" + Ytoria(lista_y) + ')'
        lista.append(formula)
            
        return Ytoria(lista)
    
    
    

    def visualizar(self, I):
        # Inicializo el plano que contiene la figura
        fig, axes = plt.subplots()
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        # Dibujo el tablero
        step = 1./8
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
        for j in range(8):
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
        arr_img = plt.imread("./img/dama.png", format='png')
        imagebox = OffsetImage(arr_img, zoom=0.1)
        imagebox.image.axes = axes
        # Creando las direcciones en la imagen de acuerdo a literal
        direcciones = {}
        direcciones[(0,0)] = [0.1, 0.1]
        direcciones[(1,0)] = [0.2, 0.1]
        direcciones[(2,0)] = [0.3, 0.1]
        direcciones[(3,0)] = [0.4, 0.1]
        direcciones[(4,0)] = [0.5, 0.1]
        direcciones[(5,0)] = [0.6, 0.1]
        direcciones[(6,0)] = [0.7, 0.1]
        direcciones[(7,0)] = [0.8, 0.1]
        #
        direcciones[(0,1)] = [0.1, 0.2]
        direcciones[(1,1)] = [0.2, 0.2]
        direcciones[(2,1)] = [0.3, 0.2]
        direcciones[(3,1)] = [0.4, 0.2]
        direcciones[(4,1)] = [0.5, 0.2]
        direcciones[(5,1)] = [0.6, 0.2]
        direcciones[(6,1)] = [0.7, 0.2]
        direcciones[(7,1)] = [0.8, 0.2]
        #
        direcciones[(0,2)] = [0.1, 0.3]
        direcciones[(1,2)] = [0.2, 0.3]
        direcciones[(2,2)] = [0.3, 0.3]
        direcciones[(3,2)] = [0.4, 0.3]
        direcciones[(4,2)] = [0.5, 0.3]
        direcciones[(5,2)] = [0.6, 0.3]
        direcciones[(6,2)] = [0.7, 0.3]
        direcciones[(7,2)] = [0.8, 0.3]
        #
        direcciones[(0,3)] = [0.1, 0.4]
        direcciones[(1,3)] = [0.2, 0.4]
        direcciones[(2,3)] = [0.3, 0.4]
        direcciones[(3,3)] = [0.4, 0.4]
        direcciones[(4,3)] = [0.5, 0.4]
        direcciones[(5,3)] = [0.6, 0.4]
        direcciones[(6,3)] = [0.7, 0.4]
        direcciones[(7,3)] = [0.8, 0.4]
        #
        direcciones[(0,4)] = [0.1, 0.5]
        direcciones[(1,4)] = [0.2, 0.5]
        direcciones[(2,4)] = [0.3, 0.5]
        direcciones[(3,4)] = [0.4, 0.5]
        direcciones[(4,4)] = [0.5, 0.5]
        direcciones[(5,4)] = [0.6, 0.5]
        direcciones[(6,4)] = [0.7, 0.5]
        direcciones[(7,4)] = [0.8, 0.5]
        #
        direcciones[(0,5)] = [0.1, 0.6]
        direcciones[(1,5)] = [0.2, 0.6]
        direcciones[(2,5)] = [0.3, 0.6]
        direcciones[(3,5)] = [0.4, 0.6]
        direcciones[(4,5)] = [0.5, 0.6]
        direcciones[(5,5)] = [0.6, 0.6]
        direcciones[(6,5)] = [0.7, 0.6]
        direcciones[(7,5)] = [0.8, 0.6]
        #
        direcciones[(0,6)] = [0.1, 0.7]
        direcciones[(1,6)] = [0.2, 0.7]
        direcciones[(2,6)] = [0.3, 0.7]
        direcciones[(3,6)] = [0.4, 0.7]
        direcciones[(4,6)] = [0.5, 0.7]
        direcciones[(5,6)] = [0.6, 0.7]
        direcciones[(6,6)] = [0.7, 0.7]
        direcciones[(7,6)] = [0.8, 0.7]
        #
        direcciones[(0,7)] = [0.1, 0.8]
        direcciones[(1,7)] = [0.2, 0.8]
        direcciones[(2,7)] = [0.3, 0.8]
        direcciones[(3,7)] = [0.4, 0.8]
        direcciones[(4,7)] = [0.5, 0.8]
        direcciones[(5,7)] = [0.6, 0.8]
        direcciones[(6,7)] = [0.7, 0.8]
        direcciones[(7,7)] = [0.8, 0.8]
        for l in I:
            if I[l]:
                x, y = self.CenC.inv(l)
                ab = AnnotationBbox(imagebox, direcciones[(x,y)], frameon=False)
                axes.add_artist(ab)
        plt.show()
