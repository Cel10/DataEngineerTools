# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
import re


class ImdbcrawlerPipeline:
        
    def process_item(self, item, spider):
        if item :
            item['classement'] = clean_spaces(item['classement'])
            item["title"] = clean_spaces(item["title"])
            item['image'] = clean_spaces(item['image'])
            item['year'] = int(clean_spaces(item['year']))
            item['synopsis'] = str_join(item['synopsis'])
            item['metascore'] = clean_spaces(item['metascore'])
            item['note'] = float(clean_spaces(item['note']))
            item['time'] = clean_spaces(item['time'])
            item['genres'] = item['genres']
            item['directors'] = item['directors']
            item['actors'] = clean_list(item['actors'])
            item['characters'] = item['characters']
            item['rang'] = find_number(item['rang'])
            #item['link'] = item['link']
            return item
        
        else :
            raise DropItem("Missing title in %s" % item)

def clean_spaces(string):
    '''
    Permet de remplacer les espaces duppliqués en un seul espace
    
    Argument : 
        string : chaine de caractères 
    
    Return : 
        La chaine de caractères sans espaces duppliqués (les espaces duppliqués sont remplacés par un seul espace)
        
    >>>clean_spaces('    he    llo')
    'he llo'
    '''
    if string:
        return " ".join(string.split())

def str_join(str_list):
    '''
    Permet d'obtenir une chaine de caractères à partir d'une liste de chaine de caractères et de supprimer les espaces duppliqués
    
    Argument : 
        str_list : liste de chaine de caractères 
    
    Return : 
        Une chaine de caractères
        
    >>>str_join(['                ','  Avengers :  ', ' Endgame  '])
    'Avengers : Endgame'
    '''
    str_list = clean_spaces(''.join(str_list))
    return str_list

def clean_list(str_list):
    '''
    Permet de supprimer le saut de ligne codé en html et et de supprimer les espaces duppliqués
    
    Argument : 
        str_list : liste de chaine de caractères 
    
    Return : 
        La liste de chaine de caractères sans les marquages html
        
    >>>clean_list([' Chris Hemsworth \n','  Chris Evans \n', ' Scarlett Johansson \n'])
    ['Chris Hemsworth','Chris Evans', 'Scarlett Johansson']
    '''
    for i in range(len(str_list)) :
        str_list[i] = clean_spaces(str_list[i].replace('\n', ''))
        
    return str_list

def find_number(str_list):
    '''
    Permet d'extraire un nombre d'une liste de chaine de caractères
    
    Argument : 
        str_list : liste de chaine de caractères 
    
    Return : 
        Un nombre int
        
    >>>find_number(['\n                    51\n      (', ' ', ')\n                '])
    51
    '''
    str_list = str_join(str_list)
    number = int(re.findall('\d+', str_list)[0])
    
    return number

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongo')
        self.db = self.client["imdb"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item