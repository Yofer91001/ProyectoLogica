import numpy as np
from declarations import casillas
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from itertools import combinations
from types import MethodType

class Formula :

    def __init__(self) :
        pass

    def __str__(self) :
        if type(self) == Letra:
            return self.letra
        elif type(self) == Negacion:
            return '-' + str(self.subf)
        elif type(self) == Binario:
            return "(" + str(self.left) + self.conectivo + str(self.right) + ")"

    def letras(self):
        if type(self) == Letra:
            return set(self.letra)
        elif type(self) == Negacion:
            return self.subf.letras()
        elif type(self) == Binario:
            return self.left.letras().union(self.right.letras())

    def subforms(self):
        if type(self) == Letra:
            return [str(self)]
        elif type(self) == Negacion:
            return list(set([str(self)] + self.subf.subforms()))
        elif type(self) == Binario:
            return list(set([str(self)] + self.left.subforms() + self.right.subforms()))

    def valor(self, I) :
        if type(self) == Letra:
            return I[self.letra]
        elif type(self) == Negacion:
            return not self.subf.valor(I)
        elif type(self) == Binario:
            if self.conectivo == 'Y':
                return self.left.valor(I) and self.right.valor(I)
            if self.conectivo == 'O':
                return self.left.valor(I) or self.right.valor(I)
            if self.conectivo == '>':
                return not self.left.valor(I) or self.right.valor(I)
            if self.conectivo == '=':
                return (self.left.valor(I) and self.right.valor(I)) or (not self.left.valor(I) and not self.right.valor(I))

    def num_conec(self):
        if type(self) == Letra:
            return 0
        elif type(self) == Negacion:
            return 1 + self.subf.num_conec()
        elif type(self) == Binario:
            return 1 + self.left.num_conec() + self.right.num_conec()
  
    

    def ver(self, D):
        '''
        Visualiza una fórmula A (como string en notación inorder) usando el descriptor D
        '''
        vis = []
        A = str(self)
        for c in A:
            if c == '-':
                vis.append(' no ')
            elif c in ['(', ')']:
                vis.append(c)
            elif c in ['>', 'Y', 'O']:
                vis.append(' ' + c + ' ')
            elif c == '=':
                vis.append(' sii ')
            else:
                try:
                    vis.append(D.escribir(c))
                except:
                    raise("¡Caracter inválido!", c)
        return ''.join(vis)

class Letra(Formula) :
    def __init__ (self, letra:str) :
        self.letra = letra

class Negacion(Formula) :
    def __init__(self, subf:Formula) :
        self.subf = subf

class Binario(Formula) :
    def __init__(self, conectivo:str, left:Formula, right:Formula) :
        assert(conectivo in ['Y','O','>','='])
        self.conectivo = conectivo
        self.left = left
        self.right = right

class Descriptor :

    '''
    Codifica un descriptor de N argumentos mediante un solo caracter
    Input:  args_lista, lista con el total de opciones para cada
                     argumento del descriptor
            chrInit, entero que determina el comienzo de la codificación chr()
    Output: str de longitud 1
    '''

    def __init__ (self,args_lista,chrInit=257) :
        self.args_lista = args_lista
        assert(len(args_lista) > 0), "Debe haber por lo menos un argumento"
        self.chrInit = chrInit
        self.rango = [chrInit, chrInit + np.prod(self.args_lista)]

    def check_lista_valores(self,lista_valores) :
        for i, v in enumerate(lista_valores) :
            assert(v >= 0), "Valores deben ser no negativos"
            assert(v < self.args_lista[i]), f"Valor debe ser menor o igual a {self.args_lista[i]}"

    def codifica(self,lista_valores) :
        self.check_lista_valores(lista_valores)
        cod = lista_valores[0]
        n_columnas = 1
        for i in range(0, len(lista_valores) - 1) :
            n_columnas = n_columnas * self.args_lista[i]
            cod = n_columnas * lista_valores[i+1] + cod
        return cod

    def decodifica(self,n) :
        decods = []
        if len(self.args_lista) > 1:
            for i in range(0, len(self.args_lista) - 1) :
                n_columnas = np.prod(self.args_lista[:-(i+1)])
                decods.insert(0, int(n / n_columnas))
                n = n % n_columnas
        decods.insert(0, n % self.args_lista[0])
        return decods

    def P(self,lista_valores) :
        codigo = self.codifica(lista_valores)
        return chr(self.chrInit+codigo)

    def inv(self,codigo) :
        n = ord(codigo)-self.chrInit
        return self.decodifica(n)


class Damas:

    '''
    Clase para representar el problema de poner
    ocho damas en un tablero de ajedrez sin que se
    puedan atacar la una a la otra.
    '''

    def __init__(self):
        self.DenC = Descriptor([8,8])
        self.DenC.escribir = MethodType(escribir_dama, self.DenC)
       

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
        
        
        lista = []
        for c in casillas:

            lista_y = list()

            for z in range(8):

                for w in range(8):
                    if w != c[1]:
                        if(abs((c[0]-z)/(c[1]-w)) == 1):
                            lista_y.append('-' + self.DenC.P([z,w]))
                
            formula = '(' + self.DenC.P([c[0],c[1]]) + ">" + Ytoria(lista_y) + ')'
            lista.append(formula)
            
        return Ytoria(lista)


    def regla4(self,x=0,y=3):
        return self.DenC.P([x,y])

    def regla5(self):
        literales = [self.DenC.P([c[0], c[1]]) for c in casillas]
        combinaciones = combinations(literales, 8)
        lista = list()
        for c in combinaciones:
            lista_y = list()
            for n in range(8):
                lista_y.append(c[n])
            
            lista.append(Ytoria(lista_y))

        return(Otoria(lista))
        
    

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
                if ord(l[-1]) >= 257 and ord(l[-1]) <= 321:
                    x, y = self.DenC.inv(l)
                    ab = AnnotationBbox(imagebox, direcciones[(x,y)], frameon=False)
                    axes.add_artist(ab)
        plt.show()


def Ytoria(lista_forms):
    form = ''
    inicial = True
    for f in lista_forms:
        if inicial:
            form = f
            inicial = False
        else:
            form = '(' + form + 'Y' + f + ')'
    return form

def Otoria(lista_forms):
    form = ''
    inicial = True
    for f in lista_forms:
        if inicial:
            form = f
            inicial = False
        else:
            form = '(' + form + 'O' + f + ')'
    return form




def inorder_to_tree(cadena:str):

    conectivos = ['Y', 'O', '>', '=']
    if len(cadena) == 1:
        return Letra(cadena)
    elif cadena[0] == '-':
        return Negacion(inorder_to_tree(cadena[1:]))
    elif cadena[0] == "(":
        counter = 0 #Contador de parentesis
        for i in range(1, len(cadena)):
            if cadena[i] == "(":
                counter += 1
            elif cadena[i] == ")":
                counter -=1
            elif cadena[i] in conectivos and counter == 0:
                return Binario(cadena[i], inorder_to_tree(cadena[1:i]),inorder_to_tree(cadena[i + 1:-1]))
    else:
        raise Exception('¡Cadena inválida!')




def escribir_dama(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    x, y  = self.inv(atomo)
    return f"La dama{neg} está en la casilla ({x},{y})"

