#! /usr/bin/env python
# -*-coding: utf-8 -*-

import re, urllib2, sys

# script permettant de lister les sous-domaines contenus dans une page web

def listeSousDomaines():
	# fonction permettant de lister les sous-domaines contenus dans la page web

	# on récupère dans une variable le contenu HTML de la page web passé en argument
	website = sys.argv[1]
	contenu = ''

	req = urllib2.Request(website)
	fd = urllib2.urlopen(req)

	contenu = str(fd.readlines())

	# on utilise une regex pour trouver le nom du domaine
	domaine = re.compile(r"(?<=www.)\w+\.\w+").search(website).group(0)

	# on utilise une regex pour trouver les liens vers des sous-domaines
	match = re.compile(r"\w+\." + re.escape(domaine)).findall(contenu)

	# on affiche le message de bienvenu
	print "============================================="
	print "      Résultats pour le site %s" %domaine
	print "============================================="
	print

	# on affiche la liste des sous-domaines en enlevant les doublons
	i = 0
	for item in set(match):
		if item.split(".")[0] != "www":
			i = i + 1
			print "Sous-domaine %s : %s" %(i, item)

if __name__ == "__main__":
	listeSousDomaines()