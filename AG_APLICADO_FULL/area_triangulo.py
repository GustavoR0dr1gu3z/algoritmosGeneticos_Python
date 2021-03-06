#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 13:09:21 2021

UNIVERSIDAD AUTÓNOMA DEL ESTADO DE MÉXICO
CENTRO UNIVERSITARIO UAEM ZUMPANGO
INGENIERÍA EN COMPUTACIÓN
ALGORITMOS GENÉTICOS 2021
TEMA: Representación de soluciones numéricas para AG con POO
ALUMNO: GUSTAVO RODRIGUEZ CALZADA
PROFESOR: ASDRÚBAL LÓPEZ CHAU

DESCRIPCIÓN: Área máxima de un triángulo



@author: gustavo
"""

from Cromosomas import Cromosoma 
import numpy as np
import copy
import random

class Triangulo:
    def __init__(self, perimetro):
        self.a = 0
        self.b = 0
        self.c = 0        
        self.perimetro = perimetro
        
    def __str__(self):
        return "a = {:.3f}, b = {:.3f} c = {:.3f}".format(self.a, self.b, self.c)
    
    def setLados(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self):
        s = self.a + self.a + self.c
        s = s/2
        tempo = s*(s-self.a)*(s-self.b)*(s-self.c)
        if tempo < 0:
            area =  -1
        else:
            area =  np.sqrt(tempo)
        return area

class TrianguloAG(Triangulo):
    
    def __init__(self, perimetro):
        super().__init__(perimetro)
        self.cromo = Cromosoma()
   
    def inicializa(self):
        p = self.perimetro
        pm = p/100
        self.cromo.inicializa([pm, pm, pm], [p, p, p], [True, True, True])
        # SE LES AGREGA EL FENOTIPO A CADA LADO
        self.a = self.cromo.fenotipo()[0]
        self.b = self.cromo.fenotipo()[1]
        self.c = self.cromo.fenotipo()[2]
        
    
    def cruzar(self, madre):        
        # SE GENERAN LOS HIJOS 
        hijos = self.cromo.cruzar(madre.cromo)
        # SELECCIONA LOS LADOS DEL HIJO0
        lados = hijos[0].fenotipo()
        a = lados[0]
        b = lados[1]
        c = lados[2]
        # SE HACE UNA COPIA DEL GEN ACTUAL
        hijo1 = copy.deepcopy(self)
        # SE AGREGAN LOS LADOS A LA FUNCION DE setLados
        hijo1.setLados(a, b, c)
        # SE HACE UNA COPIA DE LA MADRE
        hijo2 = copy.deepcopy(madre)
        # SELECCION DE LOS LADOS DEL HIJO1
        lados = hijos[1].fenotipo()
        a = lados[0]
        b = lados[1]
        c = lados[2]
        # SE AGREGAN LOS LADOS A LA FUNCION DE setLados
        hijo2.setLados(a, b, c)
        return [hijo1, hijo2]
    
    def mutar(self):
        # SE CREA UN OBJETO DE TIPO CROMO LLAMADO MUTANTE
        mutante = self.cromo
        # SE MANDA A LLAMAR SU FUNCION MUTAR, Y SOLO SE MUTA 1 BIT
        mutante.mutar(1)
        # SE GENERA SU RESPECTIVO FENOTIPO
        lados = mutante.fenotipo()
        a = lados[0]
        b = lados[1]
        c = lados[2]
        clon = copy.deepcopy(self)
        clon.setLados(a, b, c)
        return clon
    
class FitnessFunctionTriangulo:
    def evaluate(self, individuo):
        TOL = 0.5
        alfa = 1
        # SE GENERA SU AREA
        area = individuo.area()
        # PERIMETRO
        perimetroRequerido = individuo.perimetro
        perimetroInd = individuo.a + individuo.b + individuo.c
        difPerimetro = np.abs(perimetroInd - perimetroRequerido)
        if area <= 0:
            return -1
        if area > 0:
            if difPerimetro < TOL:
                return area
            else:
                return area * np.exp(-difPerimetro*alfa)


class TecnicaSeleccion:  # ESTA TECNICA ES PARA SELECCIONAR LOS MEJORES INDIVIDUOS  
    def selecciona(self, poblacion, aptitudes, cuantos):
        probs = np.exp(aptitudes)/ np.sum(np.exp(aptitudes))
        selected = random.choices(poblacion, probs, k=cuantos)
        return selected
    
class ProblemaTrianguloAG:
    
    def __init__(self, tamanoPoblacion, perimetro):
        self.N = tamanoPoblacion
        self.poblacion = []
        self.ff = FitnessFunctionTriangulo()
        self.tecSeleccion = TecnicaSeleccion()
        # 1) Genera N individuos TrianguloAG con lados aleatorios
        for i in range(self.N):
            tag = TrianguloAG(perimetro)
            tag.inicializa()
            self.poblacion.append(tag)
    
    def getAptitudes(self, pob=None): # OBTENER LA APTITUD DE CADA INDIVIDUO PARA LAS GENERACIONES
        if pob is None:
            pob = self.poblacion
        aptitudes = []
        for ind in pob:
            apt = self.ff.evaluate(ind)
            aptitudes.append(apt)
        return aptitudes # SE RETORNAN LAS APTITUDES
    
    def elitismo(self):
        # Calcula todas las aptitudes
        aptitudes = self.getAptitudes()
        # Identifica la aptitud más alta
        maxApt = np.max(aptitudes)
        # Identifica en donde está el mejor individuo
        idx = aptitudes.index(maxApt)
        # Clonar al individuo
        mejor = self.poblacion[idx]
        clon =  copy.deepcopy(mejor)
        return clon
        
    def printPoblacion(self): # SE IMPRIME TODA LA POBLACION GENERADA
        for ind in self.poblacion:
            print(ind)
    
    def evolve(self):
        sigPoblacion = []
        # 2) Aplicar elitismo
        mejor = self.elitismo()
        sigPoblacion.append(mejor)
        # 3) Cruzar para generar hijos
        pobIntermedia = []
        for i in range(int(self.N/2)):
            padres = self.tecSeleccion.selecciona(self.poblacion, self.getAptitudes(), 2)
            papa = padres[0]
            mama = padres[1]
            hijos = papa.cruzar(mama)
            hijo1 = hijos[0]
            hijo2 = hijos[1]
            pobIntermedia.append(hijo1)
            pobIntermedia.append(hijo2)
            pobIntermedia.append(copy.deepcopy(mama))
            pobIntermedia.append(copy.deepcopy(papa))
        # 4) Mutación del 5% de la población
        totalMutar = int(np.ceil(0.05*len(pobIntermedia)))
        mutantes = self.tecSeleccion.selecciona(pobIntermedia, 
                                     self.getAptitudes(pobIntermedia), 
                                     totalMutar)
        for mutante in mutantes:
            pobIntermedia.append(mutante.mutar())
        # En este punto pobIntermedia contiene padres, hijos y mutantes
        # 5) Crear nueva generación
        seleccionados = self.tecSeleccion.selecciona(pobIntermedia, self.getAptitudes(pobIntermedia), self.N-1)
        for seleccionado in seleccionados:
            clon = copy.deepcopy(seleccionado)
            sigPoblacion.append(clon)
        self.poblacion = sigPoblacion

tPob = int(input("Digite el tamaño de la poblacion: "))
nPer = int(input("Digite el perimetro a desear: "))
prob = ProblemaTrianguloAG(tPob, nPer)
print("--------------------POBLACION ORIGINAL--------")
prob.printPoblacion()
prob.evolve()
print("\n\n---------------POBLACION EVOLUCIONADA-----")
prob.printPoblacion()




















'''
class IndividuoCluster:
    def __init__(self, datos):
        self.datos = datos  # guardo los datos 
    
    def inicializa(self, K):
        longitud = len(self.datos)
        valoresAlelicos = list(range(1, K+1))
        self.cromosoma = random.choices(valoresAlelicos,
                                        k=longitud)

    def cruzar(self, madre):
        pass
    
    def mutar(self):
        pass
    
    def printIt(self):
        print(self.cromosoma)

##########################################################
#PRUEBAS
datos = pd.read_csv('iris.csv')
datos = datos.iloc[:,0:2]
plt.scatter(datos.iloc[:, 0], datos.iloc[:, 1])
ind1 = IndividuoCluster(datos)
K = 3
ind1.inicializa(K)
ind1.printIt()

'''