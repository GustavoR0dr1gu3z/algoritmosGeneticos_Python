#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 14:55:45 2021

@author: gustavo
"""

import numpy as np
import random
import math

vMin = 0
vMax = 20

v = max([vMin, vMax])

#print("Valor Máximo")
#print(v)

print("N Bits")
nbits = int(np.ceil(np.log(v + 1)/np.log(2)) + 1)
print(nbits)

#print("Numeros 0 y 1")
#cromosoma = random.choices([0, 1], k = nbits)
#print(cromosoma)

print("Numeros aleatorios punto flotante")
cromosoma = random.uniform (vMin, vMax)
print(cromosoma)



def binario(num):
    co=0
    resto = 0
    numero_binario = []
    co = num //2
    resto=num%2
    numero_binario.append(resto)
    num=num//2
    numero_binario.append(1)
    numero_binario.reverse()
    
    if num < 0:
        print("negativo: ", num)
        numero_binario.insert(0,1)
    else:
        numero_binario.insert(0,0)
    return numero_binario
 
def binario_decimal(decimal):
 
    aux=decimal*2
    decimal_binario=[]
    lista=[]
    valor=0
    while aux not in lista :
            lista.append(aux)
            partes=math.modf(aux)
            valor= int(round(partes[1],2))
            decimal_binario.append(valor)
            if int(round(partes[1],2)) == 1 and round(partes[0],2)== 0.0:
                break
            aux=round(partes[0],2) * 2
 
    return decimal_binario
 
 
 
 
def entero_decimal(numero):
    global entero
    global decimal
#    global numero
    partes=math.modf(numero)
    decimal=int(partes[0])
    entero=round(partes[1],2)
    if entero == 0:
        adada = str(binario(entero))
        print("NUMERO ENTERO: ",entero)
        cad = str(adada[1:]).replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
        print(cad)
    else:
        parte_entera=binario(entero)
        parte_decimal=binario_decimal(decimal)
        adada = str(parte_entera)+str(".")+str(parte_decimal)
        cad = str(adada[1:]).replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
        print(cad)
    return cad

print("\n\n\nHaber convertido")
conv = entero_decimal(cromosoma)
#print(conv)






