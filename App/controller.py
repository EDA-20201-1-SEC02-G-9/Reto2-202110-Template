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
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

index_by_id = {
    'video_id': 0,
    'trending_date': 1,
    'title': 2,
    'channel_title': 3,
    'category_id': 4,
    'publish_time': 5,
    'views': 6,
    'likes': 7,
    'dislikes': 8,
    'comment_count': 9,
    'thumbnail_link': 10,
    'comments_disabled': 11,
    'ratings_disabled': 12,
    'video_error_or_removed': 13,
    'description': 14,
    'country': 15
}

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.video_catalog("Data/videos-small.csv", "Data/category-id.csv")
    return catalog
# Funciones para la carga de datos


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def create_results(print_parameters, videos_list):
    print_indexes = [index_by_id[parameter] for parameter in print_parameters]
    print(print_indexes)
    result = []
    iter_video = videos_list['first']
    while iter_video:
        video = iter_video['info']
        result.append(tuple([str(lt.getElement(video[0], i+1)) for i in print_indexes]))
        iter_video = iter_video['next']
    return result

def req_4(catalog: model.video_catalog, print_parameters, tag:str, n: int):
    top = catalog.req_4(tag, n)
    return create_results(print_parameters, top)