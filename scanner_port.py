#!/usr/bin/env python
#-*- coding: utf-8 -*-

# programme prenant en argument ue adresse IP, et retournant la liste des ports ouverts parmi les ports de la liste ci-dessous

import socket, sys

# définition des ports à scanner, et des ports ouverts
ports = [21,22,25,53,80,139,443,1080,3128,8080,8081]
open_ports = []
closed_ports = []

# récupération de l'hôte à scanner
host = sys.argv[1]

# pour chaque port sur chaque port
for port in ports:

	# on crée un socket
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# on essaie de se connecter sur le port de la cible
		try:
			# en cas de succès on stock le port dans la liste des ports ouverts
			s.connect((host,port))
			open_ports.append(port)
		# si a une erreur dans l'adresse, on arrête	
		except socket.gaierror, e:
			print "Erreur d'adresse IP : %s" %e
			sys.exit(1)
		# en cas d'échec pour cause de port fermé, on stock le port dans la liste des ports fermés
		except socket.error:
			closed_ports.append(port)


	except socket.error, e:
		print "Erreur lors de la création du socket : %s" %e
		sys.exit(1)	

# on retourne la liste des ports ouverts et des ports fermés
print "Ports ouverts : %s \nPorts fermés : %s" %(open_ports, closed_ports)

