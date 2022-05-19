from declarations import *
from random import choice
from clases import inorder_to_tree
from pysat.solvers import Solver, Minisat22





def complemento(l):
    if '-' in l:
        return l[1];
    else:
        return '-' + l
        
def eliminar_literal(S, l):
    S1 = [c for c in S if l not in c]
    lc = complemento(l)
    return [[p for p in c if p != lc] for c in S1]

def extender_I(I, l):
    I1 = {k:I[k] for k in I if k != l}
    if '-' in l:
        I1[l[1:]] = False
    else:
        I1[l] = True
    return I1

def unit_propagate(S, I):
    '''
    Algoritmo para eliminar clausulas unitarias de un conjunto de clausulas, manteniendo su satisfacibilidad
    Input: 
        - S, conjunto de clausulas
        - I, interpretacion (diccionario {literal: True/False})
    Output: 
        - S, conjunto de clausulas
        - I, interpretacion (diccionario {literal: True/False})
    '''
    while [] not in S:
        l = ''
        for x in S:
            if len(x) == 1:
                l = x[0]
                S = eliminar_literal(S, l)
                I = extender_I(I, l)
                break
        if l == '': # Se recorrió todo S y no se encontró unidad
            break
    return S, I


def dpll(S, I):
    '''
    Algoritmo para verificar la satisfacibilidad de una formula, y encontrar un modelo de la misma
    Input: 
        - S, conjunto de clausulas
        - I, interpretacion (diccionario literal->True/False)
    Output: 
        - String, Satisfacible/Insatisfacible
        - I ,interpretacion (diccionario literal->True/False)
    '''
    S, I = unit_propagate(S,I)
    
    if [] in S:
        return 'insatisfacible', {}
    elif len(S) == 0:
        return 'satisfacible', I
    
        
    C = choice(S)
    l = choice(C)
    
    
    Sp = eliminar_literal(S, l)

    Ip = extender_I(I, l)
    sat, Ip = dpll(Sp, Ip)

    if( sat == "satisfacible"):
        return sat, Ip
    else:
        Spp = eliminar_literal(S, complemento(l))
        Ipp = extender_I(I, complemento(l))
        return dpll(Spp, Ipp)

def a_clausal(A):
    # Subrutina de Tseitin para encontrar la FNC de
    # la formula en la pila
    # Input: A (cadena) de la forma
    #                   p=-q
    #                   p=(qYr)
    #                   p=(qOr)
    #                   p=(q>r)
    # Output: B (cadena), equivalente en FNC
    assert(len(A)==4 or len(A)==7), u"Fórmula incorrecta!"
    B = ''
    p = A[0]
    # print('p', p)
    if "-" in A:
        q = A[-1]
        # print('q', q)
        B = "-"+p+"O-"+q+"Y"+p+"O"+q
    elif "Y" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O-"+p+"Y"+r+"O-"+p+"Y-"+q+"O-"+r+"O"+p
    elif "O" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = "-"+q+"O"+p+"Y-"+r+"O"+p+"Y"+q+"O"+r+"O-"+p
    elif ">" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O"+p+"Y-"+r+"O"+p+"Y-"+q+"O"+r+"O-"+p
    elif "=" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        #qO-rO-pY-qOrO-pY-qO-rOpYqOrOp
        B = q+"O"+"-"+r+"O"+"-"+p+"Y"+"-"+q+"O"+r+"O"+"-"+p+"Y"+"-"+q+"O"+"-"+r+"O"+p+"Y"+q+"O"+r+"O"+p
    else:
        print(u'Error enENC(): Fórmula incorrecta!')
    B = B.split('Y')
    B = [c.split('O') for c in B]
    return B

def tseitin(A):
    '''
    Algoritmo de transformacion de Tseitin
    Input: A (cadena) en notacion inorder
    Output: B (cadena), Tseitin
    '''
    # Creamos letras proposicionales nuevas
    f = inorder_to_tree(A)
    letrasp = f.letras()
    cods_letras = [ord(x) for x in letrasp]
    m = max(cods_letras) + 256
    letrasp_tseitin = [chr(x) for x in range(m, m + f.num_conec())]
    letrasp = list(letrasp) + letrasp_tseitin
    L = [] # Inicializamos lista de conjunciones
    Pila = [] # Inicializamos pila
    i = -1 # Inicializamos contador de variables nuevas
    s = A[0] # Inicializamos símbolo de trabajo
    while len(A) > 0: # Recorremos la cadena
        # print("Pila:", Pila, " L:", L, " s:", s)
        if (s in letrasp) and (len(Pila) > 0) and (Pila[-1]=='-'):
            i += 1
            atomo = letrasp_tseitin[i]
            Pila = Pila[:-1]
            Pila.append(atomo)
            L.append(atomo + "=-" + s)
            A = A[1:]
            if len(A) > 0:
                s = A[0]
        elif s == ')':
            w = Pila[-1]
            O = Pila[-2]
            v = Pila[-3]
            Pila = Pila[:len(Pila)-4]
            i += 1
            atomo = letrasp_tseitin[i]
            L.append(atomo + "=(" + v + O + w + ")")
            s = atomo
        else:
            Pila.append(s)
            A = A[1:]
            if len(A) > 0:
                s = A[0]
    if i < 0:
        atomo = Pila[-1]
    else:
        atomo = letrasp_tseitin[i]
    B = [[[atomo]]] + [a_clausal(x) for x in L]
    B = [val for sublist in B for val in sublist]
    return B

def SATsolver(A):
    
    def lit_numero(l):
        assert(ord(l[-1])!=255), f'l:{l} ///  ord:{ord(l[-1])}'
        if '-' in l:
            return -ord(l[1:]) + 255
        else:
            return ord(l) - 255
    
    def clausula_numero(C):
        return [lit_numero(l) for l in C]

    def fnc_numero(S):
        return [clausula_numero(C) for C in S]

    def obtener_int(mod):
        return {chr(255 + abs(n)):n>0 for n in mod}
        
    S = tseitin(A)
    S = fnc_numero(S)
    with Minisat22(bootstrap_with=S) as m:
        if m.solve():
            return 'Satisfacible', obtener_int(m.get_model())
        else:
            return 'Insatisfacible', {}