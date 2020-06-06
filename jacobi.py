from numpy import *
from multiprocessing.pool import ThreadPool

A = array([ [3,-1,-1],
            [-1,3,1],
            [2,1,4]])

b = array([1,3,7])

vInicio = array([0,0,0],dtype=float)

print(A)
def cuadrada(A):
    cuadro = True
    for i in range(0,len(A)):
        if(len(A)!=len(A[i])):
            cuadro = False
            break
    return cuadro

def diagonalDominante(A):
    Aux = array(A)
    suma = 0
    dominante = True
    for i in range(0,len(Aux[0])):
        for j in range(0,len(Aux[i])):
            if (Aux[i][j]<0):
               Aux[i][j] = (Aux[i][j] * (-1))
            suma = suma + Aux[i][j]
        if(Aux[i][i]<suma-Aux[i][i]):
            dominante = False
            break
        suma = 0
    return dominante

#sacamos D^-1 - L - W
def sacarD(A):
    print("Matriz D")
    x = diag(diag(A))
    print(x)
    return x

def sacarL(A):
    x = array(zeros_like(A))
    for i in range(0,len(A)):
       for j in range(0,len(A[i])):
            if(j<i):
                x[i][j] = A[i][j]
    print("matriz L")
    x = -1 * x
    print(x)
    return x

def sacarU(A):
    x = array(zeros_like(A))
    for i in range(0,len(A)):
       for j in range(0,len(A[i])):
            if(j>i):
                x[i][j] = A[i][j]
    print("matriz U")
    x = -1 * x
    print(x)
    return x

def sacarD_invertida(D):
    x = array(zeros_like(D),dtype=float)
    for i in range(0,len(x)):
        j = (1/D[i][i])
        x[i][i] = j
    print("Matriz D invertida")
    print(x)
    return x

def parte1_despeje(D,b):
    x = D.dot(b) 
    return x

def parte2_despeje(D,L,U):
    x = L + U
    y = D.dot(x)
    a = []
    b = []
    for i in range(0,len(y)):
        a = []
        for j in range(0,len(y[i])):
            if(y[i][j] != 0):
                a.append(y[i][j])
        b.append(a)
    c = array(b)
    return c

def suma_matrices(parte1,parte2):
    a = []
    a.append(parte1)
    partex = transpose(parte2)
    for i in range(0,len(partex)):
        a.append(partex[i])
    b = array(a)
    c = transpose(b)
    return c

def calculo(parte1,parte2,inicio,iteraciones):
    #para los calculos
    valoresAux = array(inicio[:])
    valorAuxiliar = 0
    for i in range(0,iteraciones):
        print(valoresAux)
        for x in range(0,len(parte2)):
            valorAuxiliar=0
            for y in range(0,len(parte2[x])):
                if(x>y):
                    inicio[x] = valorAuxiliar + (parte2[x][y]*valoresAux[y])
                    valorAuxiliar = inicio[x]
                else:
                    inicio[x] = valorAuxiliar + (parte2[x][y]*valoresAux[y+1]) 
                    valorAuxiliar = inicio[x]
            inicio[x] = inicio[x]+ parte1[x]
        valoresAux = array(inicio)
    print("resultado")
    print(inicio)

if cuadrada(A):
    print("Si es cuadrada")
    if diagonalDominante(A):
        print ("Es estrictamente de diagonal dominante")
        D = sacarD(A)
        L = sacarL(A)
        U = sacarU(A)
        d_inver = sacarD_invertida(D)
        pool = ThreadPool(processes=3)
        async_result1 = pool.apply_async(parte1_despeje, (d_inver, b))
        parte1 = async_result1.get()
        print("PARTE 1")
        print(parte1)
        async_result2 = pool.apply_async(parte2_despeje, (d_inver,L,U))
        parte2 = async_result2.get()
        print("PARTE 2")
        print(parte2)
        #Resolucion del problema
        calculo(parte1,parte2,vInicio,3)
        async_result3 = pool.apply_async(calculo, (parte1,parte2,vInicio,3))
        resultado = async_result3.get()
    else:
        print ("No es estrictamente de diagonal dominante la matriz")
else:
    print("La matriz no es cuadrada, no se puede realizar")