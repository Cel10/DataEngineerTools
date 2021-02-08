# -*- coding: Utf-8 -*-

#!/usr/bin/env python
from flask import Flask, request, render_template
from . import config

import datetime

from elasticsearch.helpers import bulk
import numpy as np
from elasticsearch import Elasticsearch
import json
import pymongo
import pandas as pd


app = Flask(__name__)

app.config.from_object(config)

# Ouverture de la base de donnA©es en dictionnaires
with open("imdb.json") as f:
    DOCUMENTS = json.load(f)

LOCAL = False
imdb_client = Elasticsearch(hosts="http://localhost", port= 9200)

def generate_data(documents):
	
    for docu in documents:
        yield {
            "_index": "imdb",
            
            "_source": {k:v if v else None for k,v in docu.items()},
        }
# helper bulk permet d'indexer tous les documents d'un seul coup
bulk(imdb_client, generate_data(DOCUMENTS))
imdb_client.indices.delete(index='imdb', ignore=[400,404])
bulk(imdb_client, generate_data(DOCUMENTS))

def movies_actor(name) :    
    
    QUERY = {
      "query": {
        "multi_match" : {
          "query": name,
          "fields": ["actors"] 
        }
      },
        "sort" : [
        { "rang" : {"order" : "asc"}}
        ]
    }
    result = imdb_client.search(index="imdb", body=QUERY)
    list_movies = [elt['_source']['title'] for elt in result["hits"]["hits"]]
    list_synop = [elt['_source']['synopsis'] for elt in result["hits"]["hits"]]
    list_img = [elt['_source']['image'] for elt in result["hits"]["hits"]]
    list_note = [elt['_source']['note'] for elt in result["hits"]["hits"]]
    
    return list_movies, list_synop, list_img, list_note

def movies_name(name) :    
    
    QUERY = {
      "query": {
        "multi_match" : {
          "query": name,
          "fields": ["title"]
        }
      },
        "sort" : [
        { "rang" : {"order" : "asc"}}
        ]
    }
    result = imdb_client.search(index="imdb", body=QUERY)
    list_movies = [elt['_source']['title'] for elt in result["hits"]["hits"]]
    list_synop = [elt['_source']['synopsis'] for elt in result["hits"]["hits"]]
    list_img = [elt['_source']['image'] for elt in result["hits"]["hits"]]
    list_note = [elt['_source']['note'] for elt in result["hits"]["hits"]]
    
    return list_movies, list_synop, list_img, list_note

def movies_charac(name) :    
    
    QUERY = {
      "query": {
        "multi_match" : {
          "query": name,
          "fields": ["characters"] 
        }
      },
        "sort" : [
        { "rang" : {"order" : "asc"}}
        ]
    }
    result = imdb_client.search(index="imdb", body=QUERY)
    list_movies = [elt['_source']['title'] for elt in result["hits"]["hits"]]
    list_synop = [elt['_source']['synopsis'] for elt in result["hits"]["hits"]]
    list_img = [elt['_source']['image'] for elt in result["hits"]["hits"]]
    list_note = [elt['_source']['note'] for elt in result["hits"]["hits"]]
    
    return list_movies, list_synop, list_img, list_note
	
def movies_direc(name) :    
    
    QUERY = {
      "query": {
        "multi_match" : {
          "query": name,
          "fields": ["directors"] 
        }
      },
        "sort" : [
        { "rang" : {"order" : "asc"}}
        ]
    }
    result = imdb_client.search(index="imdb", body=QUERY)
    list_movies = [elt['_source']['title'] for elt in result["hits"]["hits"]]
    list_synop = [elt['_source']['synopsis'] for elt in result["hits"]["hits"]]
    list_img = [elt['_source']['image'] for elt in result["hits"]["hits"]]
    list_note = [elt['_source']['note'] for elt in result["hits"]["hits"]]
    
    return list_movies, list_synop, list_img, list_note

def movies_cate(name) :    
    
    QUERY = {
      "query": {
        "multi_match" : {
          "query": name,
          "fields": ["genres"] 
        }
      },
        "sort" : [
        { "rang" : {"order" : "asc"}}
        ]
    }
    result = imdb_client.search(index="imdb", body=QUERY)
    list_movies = [elt['_source']['title'] for elt in result["hits"]["hits"]]
    list_synop = [elt['_source']['synopsis'] for elt in result["hits"]["hits"]]
    list_img = [elt['_source']['image'] for elt in result["hits"]["hits"]]
    list_note = [elt['_source']['note'] for elt in result["hits"]["hits"]]
    
    return list_movies, list_synop, list_img, list_note


# Page d'accueil et Page localhost:5000/acteur
@app.route('/')
@app.route('/index')
def rien():
	# date en temps réel
	date = datetime.datetime.now()
	d = date.day
	m = date.strftime('%B')
	y = date.year
	# les 5 meilleurs films selon leur rang
	QUERY = {
		"sort" : [
			{ "rang" : {"order" : "asc"}}
		],
		"size" : 5
	}
	result = imdb_client.search(index="imdb", body=QUERY)
	test = [elt['_source']['title']  for elt in result["hits"]["hits"]]
	return render_template("index.html", day = d, month = m, year = y, top=test)
    
# Page acteur (localhost:5000/acteur)
@app.route('/acteur', methods=['GET','POST'])
def acteur():
	# Si la requête est POST, on peut recevoir une valeur
	if request.method == 'POST':
		n_ac = request.form.get("nom_acteur")
		n_re = request.form.get("nom_real")
		n_pe = request.form.get("nom_perso")
		
		# Si c'est la case acteur qui est sélectionné (pas vide)
		if(n_ac!=None):
			name = movies_actor(n_ac)[0]
			synopsis = movies_actor(n_ac)[1]
			image = movies_actor(n_ac)[2]
			note = movies_actor(n_ac)[3]
			h2 = "Liste des films avec " + n_ac.title()
		# Si c'est la case réalisateur qui est sélectionné (pas vide)
		elif(n_re!= None):
			name = movies_direc(n_re)[0]
			synopsis = movies_direc(n_re)[1]
			image = movies_direc(n_re)[2]
			note = movies_direc(n_re)[3]
			h2 = "Liste des films de " + n_re.title()
		# Si c'est la case personnage qui est sélectionné (pas vide)
		elif(n_pe!=None):
			name = movies_charac(n_pe)[0]
			synopsis = movies_charac(n_pe)[1]
			image = movies_charac(n_pe)[2]
			note = movies_charac(n_pe)[3]
			h2 = "Liste des films avec le personnage " + n_pe.title()
			
		# Si le résultat est null 
		if(len(name)==0):
			h2 = "Ta recherche ne fait pas partie des 200 films les plus populaires, sorry !"
		
		return render_template('acteur.html', h2=h2, nom=name, synopsis=synopsis, image=image, note=note)
	# Si on recoit rien
	return render_template('acteur.html')

# Page film (localhost:5000/film)
@app.route('/film',methods = ['POST', 'GET'])
def film():
	# Si la requête est POST, on peut recevoir une valeur
	if request.method == 'POST':
		t = request.form.get("titre")
		titre = movies_name(t)[0]
		synopsis = movies_name(t)[1]
		image = movies_name(t)[2]
		note = movies_name(t)[3]
		# Si le résultat est null 
		if(len(titre)==0):
			h2 = "Ta recherche ne fait pas partie des 200 films les plus populaires, sorry !"
		else:
			h2 = "Liste des films"
		
		return render_template('film.html', h2=h2, titre=titre, synopsis=synopsis, image=image, note=note)
	# Si on recoit rien
	return render_template("film.html")
	
# Page catégorie (localhost:5000/categorie)
@app.route('/categorie',methods = ['POST', 'GET'])
def categorie():
	# Si la requête est POST, on peut recevoir une valeur
	if request.method == 'POST':
		c = request.form.get("categorie")
		category = movies_cate(c)[0]
		synopsis = movies_cate(c)[1]
		image = movies_cate(c)[2]
		note = movies_cate(c)[3]
		# Si le résultat est null 
		if(len(category)==0):
			h2 = "Cette categorie n'existe pas, sorry ! (ou il y a une erreur dans le mot)"
		else:
			h2 = "Liste des films de genre " + c.title() + " tries selon leur popularite"
		
		return render_template('categorie.html', h2=h2, category=category, synopsis=synopsis, image=image, note=note)
	# Si on recoit rien
	return render_template("categorie.html")	
	
# Appel au lancement de l'application
if __name__ == "__main__":
    app.run()
	





