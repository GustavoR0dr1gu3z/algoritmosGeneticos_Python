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
from Cromosomas import GenReal
import numpy as np

class Triangulo:
    def __init__(self, perimetro):
        self.perimetro = perimetro;
        
    def setLados(self,a,b,c):
        self.a = a
        self.a = b
        self.a = c
        
