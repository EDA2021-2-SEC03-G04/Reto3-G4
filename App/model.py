"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as m
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    catalog = {'UFOSByCity': None
        
                }

    
    catalog['UFOSByCity'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareCities)
    return catalog

# Funciones para agregar informacion al catalogo

def addUFO(catalog,UFO):
    new=newUFO(UFO['datetime'],UFO['city'],UFO['state'],UFO['country'],UFO['shape'],UFO['duration (seconds)'],UFO['duration (hours/min)'],UFO['comments'],UFO['date posted'],UFO['latitude'],UFO['longitude'])

    #Crea el tree de UFOS por ciudades
    City=UFO['city']

    if om.contains(catalog['UFOSByCity'],City):
        listavieja=om.get(catalog['UFOSByCity'],City)
        lt.addLast(listavieja['value'],new)
        om.put(catalog['UFOSByCity'],City,listavieja['value'])
    else: 
        lista=lt.newList()
        lt.addLast(lista,new)
        om.put(catalog['UFOSByCity'],City,lista)

# Funciones para creacion de datos

def newUFO(datetime,city,state,country,shape,durationS,durationHM,comments,dateposted,latitude,longitude):

    UFO={'datetime':'','city':'','state':'','country':'','shape':'','durationS':'','durationHM':''
    ,'comments':'','dateposted':'','latitude':'','longitude':''}

    UFO['datetime']=datetime
    UFO['city']=city
    UFO['state']=state
    UFO['country']=country
    UFO['shape']=shape
    UFO['durationS']=durationS
    UFO['durationHM']=durationHM
    UFO['comments']=comments
    UFO['dateposted']=dateposted
    UFO['latitude']=latitude
    UFO['longituide']=longitude



# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareCities(UFO1,UFO2):
    '''
    Compara ciudades
    '''
    ufo1=lt.getElement(UFO1,1)
    ufo2=lt.getElement(UFO2,1)
    city1=ufo1['city']
    city2=ufo2['city']
    if (city1.lower()==city2.lower()):
        return 0
    elif (city1.lower() > city2.lower()):
        return 1
    else:
        return -1

# Funciones de ordenamiento
