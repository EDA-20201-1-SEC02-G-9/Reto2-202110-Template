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
from DISClib.DataStructures import linkedlistiterator as lliterator
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

index_by_id = {
    'video_id': 1,
    'trending_date': 2,
    'title': 3,
    'channel_title': 4,
    'category_id': 5,
    'publish_time': 6,
    'views': 7,
    'likes': 8,
    'dislikes': 9,
    'comment_count': 10,
    'thumbnail_link': 11,
    'comments_disabled': 12,
    'ratings_disabled': 13,
    'video_error_or_removed': 14,
    'description': 15,
    'country': 16,
    'tags': 17
}

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.video_catalog("Data/videos-all.csv", "Data/category-id.csv")
    return catalog
# Funciones para la carga de datos


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def tags_to_str(tags):
    iter_tags = lliterator.newIterator(tags)
    res = ""
    while lliterator.hasNext(iter_tags):
        res += lliterator.next(iter_tags) + ","
    return res

def create_results(print_parameters, videos_list):
    print_indexes = [index_by_id[parameter] for parameter in print_parameters]
    print(print_indexes)
    result = []
    iter_video = videos_list['first']
    while iter_video:
        video = iter_video['info']
        result.append(
            tuple([
                str(lt.getElement(video[0], i)) if i < 17
                else tags_to_str(video[1])
                for i in print_indexes])
            )
        iter_video = iter_video['next']
    return result

def req_1(catalog: model.video_catalog, print_parameters, country:str, category:int, n: int):
    top = catalog.req_1(country, category, n)
    return create_results(print_parameters, top)

def req_2(catalog: model.video_catalog, print_parameters, country:str):
    top = catalog.req_2(country)
    return (create_results(print_parameters, top[0]), top[1])

def req_3(catalog: model.video_catalog, print_parameters, category:str):
    top = catalog.req_3(category)
    return (create_results(print_parameters, top[0]), top[1])


def req_4(catalog: model.video_catalog, print_parameters, country:str, tag:str, n: int):
    top = catalog.req_4(country, tag, n)
    return create_results(print_parameters, top)