#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 13:15:06 2021
UNIVERSIDAD AUTÓNOMA DEL ESTADO DE MÉXICO
CENTRO UNIVERSITARIO UAEM ZUMPANGO
INGENIERÍA EN COMPUTACIÓN
ALGORITMOS GENÉTICOS 2021
TEMA: Solucion de problemas con AG
ALUMNO: GUSTAVO RODRIGUEZ CALZADA
PROFESOR: ASDRÚBAL LÓPEZ CHAU

DESCRIPCIÓN: EXAMEN:Implementa clustering con un AG

@author: gustavo
"""


import pandas as pd
from matplotlib import pyplot as plt
import random
import numpy as np
from random import sample
import copy

class Cluster:
    def __init__(self, datos, k):
        # Inicializando los datos 
        self.datos = datos
        
        # Inicializando los k clusters
        self.k = k
 
        # Calcular la longitud de todos los datos       
        longitud = len(self.datos)
        
        # Valores alelicos que son numeros aleatorios del 1 al Numero de clusters
        valoresAlelicos = list(range(1, self.k+1))
        
        # Se asigna al cromosoma los valores alelicos
        self.cromosoma = random.choices(valoresAlelicos, k=longitud)
    
    
    def aptitud(self):
        # Seleccion de los indices de los elementos para el cluster
        
        datos = sample(range(0,len(self.cromosoma)),k = self.k)
        E = []
        S = []
        # Seleccionar la suma minima
        for i in range(1,len(datos)):
            for j in range(0,len(self.cromosoma)):
                E.append( pow( ( abs(self.cromosoma[j] - self.cromosoma[datos[i]]) ) ,2 ) )
            S.append(min(E))
        res = min(S)
        return res
    
    def cruzar(self,Madre):
        # Creacion de los padres y madres
        padre = self.cromosoma
        madre = Madre.cromosoma
        # Selección de las capas1 y 2 para la cruza entre dos puntod
        cp1 = int(np.ceil(len(padre)/3.0))
        cp2 = cp1*2
        # Copia de los padres y madres para modificar las copias
        hijo1 = padre.copy()
        hijo2 = madre.copy()
        # Sacar los medios
        medio1 = madre[cp1:cp2]
        medio2 = padre[cp1:cp2]
        # Asignar a los medios los puntos en los hijos 
        hijo1[cp1:cp2] = medio1
        hijo2[cp1:cp2] = medio2
        # Crea una copia exacta
        h1 = copy.deepcopy(self)  
        h1.cromosoma = hijo1
        h2 = copy.deepcopy(Madre)
        h2.cromosoma = hijo2
        # Retorno de los hijos
        return [h1, h2]        
    
    def mutar(self):
        # Mutación al 5%
        porcentaje = int( np.ceil(len(self.cromosoma)*0.05) )
        
        # Mutar aleatoriamente a los alelos por 1,2 o 3, pero no el mismo
        for i in range(porcentaje):
            #Seleccion de los indices para modificarlos
            indices = random.randint(1,len(self.cromosoma)-1)
            
            # Si en ese indice el alelo del cromosoma es == 1(Cluster) 
            if self.cromosoma[indices] == 1:                
                # Le asigna un valor aleatorio entre 2 y 3, pero NO 1
                indices2 = random.randint(2,3)                            
                self.cromosoma[indices] = self.cromosoma[indices2]

                # Si en ese indice el alelo del cromosoma es == 2(Cluster)                

            elif self.cromosoma[indices] == 2:                                
                # Le asigna valores de 1 y 3 aleatorios, pero NO 2                
                indices2 = random.sample([1,3],1)
                indices2 = int(indices2[0])
                self.cromosoma[indices] = self.cromosoma[indices2]
                
                # Si en ese indice el alelo del cromosoma es == 3(Cluster)
            elif self.cromosoma[indices] == 3:
                # Le asigna valores de 1 y 2 aleatorios, pero NO 3
                indices2 = random.randint(1,2)
                self.cromosoma[indices] = self.cromosoma[indices2]
            else:
                self.cromosoma = self.cromosoma
        # Se retorna el cromosoma                
        return self.cromosoma

     
    def graficar(self):
        labels=['','or', 'ob', 'og', 'oc', 'ok']
        clusters = list(set(self.cromosoma))
        clusters.sort()
        for cluster in clusters:
            i = 0
            index = []
            for gen in self.cromosoma:
                if gen == cluster:
                    index.append(i)
                i+=1    
            
            plt.plot(self.datos.iloc[index, 0], self.datos.iloc[index, 1], labels[cluster])
            plt.legend(labels[cluster])
             
    def __str__(self):
        # Imprimir el cromosoma con su respectiva aptitud
        inds = str(self.cromosoma)+str(self.aptitud())
        
        # Declarar variables para el contador de cuantos clusters hay
        countC1 = []
        countC2 = []
        countC3 = []
        indC1 = []
        indC2 = []
        indC3 = []
        
        for i in self.cromosoma:
            # Si hay un elemento que es del cluster 1, que lo agregue
            if i == 1:
                countC1.append(1)
            # Si hay un elemento que es del cluster 2, que lo agregue
            elif i == 2:
                countC2.append(1)
            # Si hay un elemento que es del cluster 3, que lo agregue
            else:
                countC3.append(1)
                
                    
        for i in range(len(self.cromosoma)):
            # Si en el indice i de cromosoma es 1: entonces que agregue i
            if self.cromosoma[i] == 1:
                indC1.append(i)
            # Si en el indice i de cromosoma es 2: entonces que agregue i
            elif self.cromosoma[i] == 2:
                indC2.append(i)
            # Si en el indice i de cromosoma es 3: entonces que agregue i
            else:
                indC3.append(i)
            
            # Se imprime la longitud de cada cluster, para ver cuandos hay de cada uno                
            cadena1 = "Cluster1: {}, Cluster2: {}, Cluster3: {}".format(len(countC1),len(countC2), len(countC3))
            # Se imprimen los indices de los clusters
            cadena2 = "Indices C1: {},\nIndices C2: {},\nIndices C3: {}".format(indC1, indC2, indC3)
            cadt = "\nCUANTOS ELEMENTOS DE CADA CLUSTER HAY:\n"+str(cadena1)+"\n\nINDICES DE CADA CLUSTER:\n"+str(cadena2)+"\n\nCROMOSOMA:\n"+str(inds)
        return cadt
    
    
    
    
class Cromosoma:
    def inicializa(self,numI):
        # Importamos los datos del csv    
        datos = pd.read_csv('datosExamen.csv')    
        
        #----------------AQUI SE ASIGNAN LOS NUMEROS DE CLUSTERS---------------
        # K = 3, el núero de clusters
        k = 3

        #CREACION DE LOS INDIVIDUOS
        ind = []
        for i in range(numI):
            c = Cluster(datos, k)
            ind.append(c)
        self.ind = ind
    
    def mutar(self):
        # Mutar cada uno de los individuos que hay 
        for gen in self.ind:
            gen.mutar()
            
    def cruzar(self, otro):
        # Hacer la cruza del padre y madre, que retorna 2 hijos
        # Se hace copia exacta de los objetos
        h1 = copy.deepcopy(self)
        h2 = copy.deepcopy(otro)        
        genesHijos1 = []
        genesHijos2 = []
        # Siempre genera mejores hijos
        for i in range(len(self.ind)):
            GenPadre = self.ind[i]
            GenMadre = otro.ind[i]
            genHijos = GenPadre.cruzar(GenMadre)
            genesHijos1.append(genHijos[0])
            genesHijos2.append(genHijos[1])
        h1.ind = genesHijos1
        h2.ind = genesHijos2
        return [h1, h2]

    
    def aptitudes(self):
        # Calcular su Aptitud de cada uno
        apt = []
        for gen in self.ind:
            apt.append(gen.aptitud())
        return apt


    def __str__(self):
        # Imprimirlos dando 2 saltos de línea
        cad = ""
        for gen in self.ind:
            cad = cad + str(gen) + "\n\n"
        return cad
    
    def graficar(self):
        # Graficar cada uno de los individuos
        for gen in self.ind:
            gen.graficar()
    
    
    
# CREACION DE PADRES Y MADRES    
p = Cromosoma()
m = Cromosoma()

# INICIALIZARLO CON N INDIVIDUOS, EN ESTE CASO 1 (PUEDEN SER N)
p.inicializa(1)    
m.inicializa(1)    

print('-------------Padre:-------------')
print(p)
print('-------------Madre:-------------')
print(m)
    
# Cruza del padre y madre, para la generación de 2 hijos
hijos = p.cruzar(m)
print('-------------Hijo 0:-------------')
print(hijos[0])
print('-------------Hijo 1:-------------')
print(hijos[1])

# --------------------SE HACE LA MUTACIÓN AL 5% -----------------------
# Muta el primer hijo
print('-------------Mutación al Primer Hijo--------------')
print('-------------Original:-------------')
print(hijos[0])

print('-------------Modificado:-------------')
hijos[0].mutar()
print(hijos[0])    

# Muta el segundo hijo
print('-------------Mutación al Segundo Hijo-------------')
print('-------------Original:-------------')
print(hijos[1])

print('-------------Modificado:-------------')
hijos[1].mutar()
print(hijos[1])    

# GRAFICAR HIJOS
hijos[0].graficar()
hijos[1].graficar()

