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
        #r1 = self.regla1()
        #r2 = self.regla2()
        #r3 = self.regla3()
        #self.reglas = [r1, r2, r3]

    '''
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
    
    '''
    

    def visualizar(self, I):
        # Inicializo el plano que contiene la figura
        fig, axes = plt.subplots()
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        # Dibujo el tablero
        step = 1./8
        tangulos = []
        # Creo los cuadrados claros en el tablero
        blanco = True
        for x in range(8):
            for y in range (8):
                if blanco:
                    tangulos.append(patches.Rectangle(\
                                                (x * step, y *step), \
                                                step, \
                                                step,\
                                                facecolor='cornsilk')\
                                                )
                    blanco = False
                else:
                    tangulos.append(patches.Rectangle(\
                                                (x * step, y * step), \
                                                step, \
                                                step,\
                                                facecolor='lightslategrey')\
                                                )
                    blanco = True
            

            if blanco:
                blanco = False
            else:
                blanco = True
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
        imagebox = OffsetImage(arr_img, zoom=0.015)
        imagebox.image.axes = axes
        # Creando las direcciones en la imagen de acuerdo a literal
        direcciones = {}
        direcciones[(0,0)] = [0.07, 0.07]
        direcciones[(1,0)] = [0.195, 0.07]
        direcciones[(2,0)] = [0.32, 0.07]
        direcciones[(3,0)] = [0.445, 0.07]
        direcciones[(4,0)] = [0.57, 0.07]
        direcciones[(5,0)] = [0.695, 0.07]
        direcciones[(6,0)] = [0.82, 0.07]
        direcciones[(7,0)] = [0.945, 0.07]
        #
        direcciones[(0,1)] = [0.07, 0.195]
        direcciones[(1,1)] = [0.195, 0.195]
        direcciones[(2,1)] = [0.32, 0.195]
        direcciones[(3,1)] = [0.445, 0.195]
        direcciones[(4,1)] = [0.57, 0.195]
        direcciones[(5,1)] = [0.695, 0.195]
        direcciones[(6,1)] = [0.82, 0.195]
        direcciones[(7,1)] = [0.945, 0.195]
        #
        direcciones[(0,2)] = [0.07, 0.32]
        direcciones[(1,2)] = [0.195, 0.32]
        direcciones[(2,2)] = [0.32, 0.32]
        direcciones[(3,2)] = [0.445, 0.32]
        direcciones[(4,2)] = [0.57, 0.32]
        direcciones[(5,2)] = [0.695, 0.32]
        direcciones[(6,2)] = [0.82, 0.32]
        direcciones[(7,2)] = [0.945, 0.32]
        #
        direcciones[(0,3)] = [0.07, 0.445]
        direcciones[(1,3)] = [0.195, 0.445]
        direcciones[(2,3)] = [0.32, 0.445]
        direcciones[(3,3)] = [0.445, 0.445]
        direcciones[(4,3)] = [0.57, 0.445]
        direcciones[(5,3)] = [0.695, 0.445]
        direcciones[(6,3)] = [0.82, 0.445]
        direcciones[(7,3)] = [0.945, 0.445]
        #
        direcciones[(0,4)] = [0.07, 0.57]
        direcciones[(1,4)] = [0.195, 0.57]
        direcciones[(2,4)] = [0.32, 0.57]
        direcciones[(3,4)] = [0.445, 0.57]
        direcciones[(4,4)] = [0.57, 0.57]
        direcciones[(5,4)] = [0.695, 0.57]
        direcciones[(6,4)] = [0.82, 0.57]
        direcciones[(7,4)] = [0.945, 0.57]
        #
        direcciones[(0,5)] = [0.07, 0.695]
        direcciones[(1,5)] = [0.195, 0.695]
        direcciones[(2,5)] = [0.32, 0.695]
        direcciones[(3,5)] = [0.445, 0.695]
        direcciones[(4,5)] = [0.57, 0.695]
        direcciones[(5,5)] = [0.695, 0.695]
        direcciones[(6,5)] = [0.82, 0.695]
        direcciones[(7,5)] = [0.945, 0.695]
        #
        direcciones[(0,6)] = [0.07, 0.82]
        direcciones[(1,6)] = [0.195, 0.82]
        direcciones[(2,6)] = [0.32, 0.82]
        direcciones[(3,6)] = [0.445, 0.82]
        direcciones[(4,6)] = [0.57, 0.82]
        direcciones[(5,6)] = [0.695, 0.82]
        direcciones[(6,6)] = [0.82, 0.82]
        direcciones[(7,6)] = [0.945, 0.82]
        #
        direcciones[(0,7)] = [0.07, 0.945]
        direcciones[(1,7)] = [0.195, 0.945]
        direcciones[(2,7)] = [0.32, 0.945]
        direcciones[(3,7)] = [0.445, 0.945]
        direcciones[(4,7)] = [0.57, 0.945]
        direcciones[(5,7)] = [0.695, 0.945]
        direcciones[(6,7)] = [0.82, 0.945]
        direcciones[(7,7)] = [0.945, 0.945]
        for l in I:
            if I[l]:
                x, y = self.DenC.inv(l)
                ab = AnnotationBbox(imagebox, direcciones[(x,y)], frameon=False)
                axes.add_artist(ab)
        plt.show()
