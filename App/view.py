"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Buscar video con más views")
    print("3- Más días trending (Pais)")
    print("4- Más días trending (Categoría)")
    print("5- Buscar los videos con más Likes")

catalog = None

def printResults(parameters,result):
    size = len(parameters)
    str_format = ''
    indexes = [str(i) for i in range(0, size)]
    str_format = '{'+':^20s}   {'.join(indexes) + ':^20s}'
    print(str_format.format(*tuple(parameters)))
    for line in result:
        print(str_format.format(*tuple(line)))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog= controller.initCatalog()
        dir = None
        # get first element of catalog
        for x in catalog:
            dir = x[0]['elements']
            break
        print("\nPrimer video: ",dir[2])
        print("Canal: ", dir[3])
        print("Fecha de tendencia: ",dir[1])
        print("País: ",dir[-1])
        print("vistas: ",dir[6])
        print("Likes: ",dir[7])
        print("Dislikes: ",dir[8],"\n")
        print("Id  Nombre")
        for a in catalog.tags["elements"]:
            print (a[0],"  ",a[1])
    elif int(inputs[0]) == 2:
        country = input("Introduzca el pais que quiere consultar: ")
        category = int(input("Introduzca la categoria que quiere consultar: "))
        n = int(input("Introduzca n: "))
        print_parameters = ['title', 'channel_title', 'publish_time', 'views', 'likes', 'dislikes']
        result = controller.req_1(catalog, print_parameters, n=n, category=category, country=country)
        printResults(print_parameters, result)
    elif int(inputs[0]) == 3:
        country = input("Introduzca el pais que quiere consultar: ")
        print_parameters = ['title', 'channel_title', 'publish_time', 'views', 'likes', 'dislikes']
        result = controller.req_2(catalog, print_parameters, country)
        printResults(print_parameters, result[0])
        print("Repeticiones",result[1])
    elif int(inputs[0]) == 4:
        category = int(input("Introduzca la categoria que quiere consultar: "))
        print_parameters = ['title', 'channel_title', 'publish_time', 'views', 'likes', 'dislikes']
        result = controller.req_3(catalog, print_parameters, category)
        printResults(print_parameters, result[0])
        print("Repeticiones",result[1])
    elif int(inputs[0]) == 5:
        country = input("Introduzca el pais que quiere consultar: ")
        tag = input("Introduzca el tag que quiere consultar: ")
        n = int(input("Introduzca n: "))
        print_parameters = ['title', 'channel_title', 'publish_time', 'views', 'likes', 'dislikes', 'tags']
        result = controller.req_4(catalog, print_parameters, n=n, tag=tag, country=country)
        printResults(print_parameters, result)
    else:
        sys.exit(0)
sys.exit(0)
