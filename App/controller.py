﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import time
import datetime


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog



# Funciones para la carga de datos

def loadData(catalog): 
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    StartTime=time.process_time()
    loadUfos(catalog)
    StopTime=time.process_time()
    TimeMseg=(StopTime-StartTime)*1000
    print()
    print(f'La carga de datos tardó {TimeMseg} miliseg')
    print()

def loadUfos(catalog):
    """
    Carga los artistas archivo.  .
    """
    ufosfile = cf.data_dir + 'UFOS/UFOS-utf8-large.csv'
    input_file = csv.DictReader(open(ufosfile, encoding='utf-8'))
    for ufo in input_file:
        model.addUFO(catalog, ufo)


# Funciones de ordenamiento

def AvistamienCiudad(catalog,ciudad):
    return model.AvistamienCiudad(catalog,ciudad)

def AvistamientoHHMM(catalog,liminf,limsup):
    #try:
        #liminfd =datetime.datetime.strptime(liminf, '%H:%M')
        #limsupd= datetime.datetime.strptime(limsup, '%H:%M')
        #return model.AvistamientoHHMM(catalog,liminfd,limsupd)
    #except:
        #print('Ingrese un formato de fecha adecuado.')
    liminfd =datetime.datetime.strptime(liminf, '%H:%M')
    limsupd= datetime.datetime.strptime(limsup, '%H:%M')
    return model.AvistamientoHHMM(catalog,liminfd,limsupd)

def AvistamientoAMD(catalog,liminf,limsup):


    liminfd=datetime.datetime.strptime(liminf,'%d/%m/%Y')
    limsupd=datetime.datetime.strptime(limsup,'%d/%m/%Y')

    return model.AvistamientoAMD(catalog,liminfd,limsupd)




# Funciones de consulta sobre el catálogo

def citiesSize(catalog):
    """
    Numero de crimenes leidos
    """
    return model.citiesSize(catalog)


def indexHeight(catalog):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(catalog)


def indexSize(catalog):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(catalog)


def minKey(catalog):
    """
    La menor llave del arbol
    """
    return model.minKey(catalog)


def maxKey(catalog):
    """
    La mayor llave del arbol
    """
    return model.maxKey(catalog)
